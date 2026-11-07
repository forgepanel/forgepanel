<?php
declare(strict_types=1);
require __DIR__.'/bootstrap.php';
require __DIR__.'/MemoryRepository.php';
use ForgePanel\Setup\{SetupService,SecretBox,Totp,Configuration};
use ForgePanelTests\{MemoryRepository,MutableClock};
$tests=[];$assertions=0;
function check(bool $condition,string $message='Assertion failed'):void { global $assertions; $assertions++; if(!$condition){throw new RuntimeException($message);} }
function throws(callable $fn,string $class=Throwable::class):void { try{$fn();}catch(Throwable $e){check($e instanceof $class,'Unexpected exception '.$e::class);return;}throw new RuntimeException('Expected exception not thrown'); }
function test(string $name,callable $fn):void {global $tests;$tests[$name]=$fn;}
function fixture():array {
    $repo=new MemoryRepository();$clock=new MutableClock();$box=new SecretBox(base64_encode(random_bytes(32)));$totp=new Totp();
    return [new SetupService($repo,$box,$totp,$clock),$repo,$clock,$totp,$box];
}
function registered():array {
    [$service,$repo,$clock,$totp,$box]=fixture();$token=$service->issue();
    $res=$service->register($token,'Owner@example.com','A deliberately long passphrase!');
    check($res['ok']); return [$service,$repo,$clock,$totp,$box,$res['grant'],$token];
}
function configured():array {
    [$s,$r,$clock,$totp,$box,$grant,$token]=registered();
    $e=$s->enrollment($grant);$ok=$s->confirmMfa($grant,$totp->code($e['secret'],$clock->now()));check($ok['ok']);
    return [$s,$r,$clock,$totp,$box,$grant,$token];
}
function config():array {return ['schema_version'=>1,'admin_port'=>8447,'user_port'=>8446,'admin_host'=>'forge.example.com','user_host'=>'panel.example.com','webstack'=>'nginx_apache_fpm','modules'=>['sftp','backup']];}

test('issued token is hashed, expiring and never audited',function(){[$s,$r,$c]=fixture();$t=$s->issue();check(strlen($t)===43);check($r->data->state['token_hash']===hash('sha256',$t));check($r->data->state['token_expiry']===$c->now()+900);check(!str_contains(json_encode($r->data),$t));});
test('registration consumes token and creates exactly one pending-MFA account',function(){[$s,$r,$c,$totp,$box,$g,$t]=registered();check(count($r->data->admins)===1);$a=array_values($r->data->admins)[0];check($a['email']==='owner@example.com');check(password_verify('A deliberately long passphrase!',$a['password_hash']));check($a['mfa_enabled']===false);check($r->data->state['token_hash']===null);check($r->data->state['phase']==='MFA_PENDING');check(!$s->register($t,'other@example.com','Another long passphrase!')['ok']);check(count($r->data->admins)===1);throws(fn()=>$s->issue(),DomainException::class);});
test('failed token attempts persist and lock at five',function(){[$s,$r]=fixture();$t=$s->issue();for($i=0;$i<5;$i++){check(!$s->register('wrong','a@example.com','Long enough password!')['ok']);}check($r->data->state['attempts']===5);check(!$s->register($t,'a@example.com','Long enough password!')['ok']);});
test('local regeneration invalidates a previous unconsumed token',function(){[$s,$r]=fixture();$a=$s->issue();$b=$s->issue();check($a!==$b);check(!$s->register($a,'a@example.com','Long enough password!')['ok']);check($s->register($b,'a@example.com','Long enough password!')['ok']);});
test('expiry boundary rejects the token',function(){[$s,$r,$c]=fixture();$t=$s->issue();$c->time+=900;check(!$s->register($t,'a@example.com','Long enough password!')['ok']);});
test('database failure does not consume token or partially create an account',function(){[$s,$r]=fixture();$t=$s->issue();$r->data->failAfterInsert=true;throws(fn()=>$s->register($t,'a@example.com','Long enough password!'));check($r->data->state['phase']==='TOKEN_ISSUED');check(count($r->data->admins)===0);$r->data->failAfterInsert=false;check($s->register($t,'a@example.com','Long enough password!')['ok']);});
test('validation does not consume a good token',function(){[$s,$r]=fixture();$t=$s->issue();throws(fn()=>$s->register($t,'bad','short'),InvalidArgumentException::class);check($r->data->state['phase']==='TOKEN_ISSUED');throws(fn()=>$s->register($t,'a@example.com','short'),InvalidArgumentException::class);});
test('setup capability is required on every protected operation',function(){[$s,$r,$c,$totp,$box,$g]=registered();throws(fn()=>$s->progress('wrong'),DomainException::class);throws(fn()=>$s->enrollment('wrong'),DomainException::class);throws(fn()=>$s->confirmMfa('wrong','123456'),DomainException::class);throws(fn()=>$s->saveConfiguration('wrong',config(),0),DomainException::class);});
test('security choice blocks configuration until explicitly completed',function(){[$s,$r,$c,$totp,$box,$g]=registered();throws(fn()=>$s->saveConfiguration($g,config(),0),DomainException::class);});
test('explicit MFA skip allows configuration and deletes pending secret',function(){
    [$s,$r,$c,$totp,$box,$g]=registered();
    throws(fn()=>$s->saveConfiguration($g,config(),0),DomainException::class);
    $s->skipMfa($g);
    $a=array_values($r->data->admins)[0];
    check($a['mfa_enabled']===false);
    check($a['mfa_secret']===null);
    check($a['recovery_hashes']===[]);
    check($s->progress($g)['phase']==='CONFIGURING');
    check($s->saveConfiguration($g,config(),0)['revision']===1);
    check(in_array('setup.mfa_skipped',array_column($r->data->events,0),true));
    throws(fn()=>$s->skipMfa($g),DomainException::class);
    throws(fn()=>$s->enrollment($g),DomainException::class);
});
test('MFA skip needs the current setup grant and survives local resume',function(){
    [$s,$r,$c,$totp,$box,$g]=registered();
    throws(fn()=>$s->skipMfa('invalid'),DomainException::class);
    $s->skipMfa($g);
    $code=$s->resume();
    throws(fn()=>$s->progress($g),DomainException::class);
    $res=$s->redeemResume($code);
    check($res['ok'] && $res['phase']==='CONFIGURING');
    check($s->saveConfiguration($res['grant'],config(),0)['revision']===1);
});
test('MFA validates, encrypts secret and generates hashed recovery codes',function(){[$s,$r,$c,$totp,$box,$g]=registered();$e=$s->enrollment($g);$a=array_values($r->data->admins)[0];check(!str_contains($a['mfa_secret'],$e['secret']));$res=$s->confirmMfa($g,$totp->code($e['secret'],$c->now()));check($res['ok']);check(count($res['recovery_codes'])===10);check(count(array_unique($res['recovery_codes']))===10);foreach($res['recovery_codes'] as $code){check(!str_contains(json_encode($r->data),$code));}check($s->progress($g)['phase']==='CONFIGURING');check(!$s->confirmMfa($g,$totp->code($e['secret'],$c->now()))['ok']);throws(fn()=>$s->enrollment($g),DomainException::class);});
test('MFA locks after five invalid attempts',function(){[$s,$r,$c,$totp,$box,$g]=registered();for($i=0;$i<5;$i++){check(!$s->confirmMfa($g,'not-a-code')['ok']);}$e=$s->enrollment($g);check(!$s->confirmMfa($g,$totp->code($e['secret'],$c->now()))['ok']);});
test('expired grant is rejected and local resume rotates it',function(){[$s,$r,$c,$totp,$box,$g]=registered();$c->time+=1800;throws(fn()=>$s->progress($g),DomainException::class);$code=$s->resume();$res=$s->redeemResume($code);check($res['ok']);$g2=$res['grant'];check($g2!==$g);check($s->progress($g2)['phase']==='MFA_PENDING');check(!$s->redeemResume($code)['ok']);throws(fn()=>$s->progress($g),DomainException::class);check(count($r->data->admins)===1);});
test('recovery invalidates existing grants and locks after five attempts',function(){[$s,$r,$c,$totp,$box,$g]=registered();$code=$s->resume();throws(fn()=>$s->progress($g),DomainException::class);for($i=0;$i<5;$i++){check(!$s->redeemResume('wrong')['ok']);}check(!$s->redeemResume($code)['ok']);});
test('recovery code expires at fifteen minutes',function(){[$s,$r,$c]=registered();$code=$s->resume();$c->time+=900;check(!$s->redeemResume($code)['ok']);});
test('resume is not allowed before registration',function(){[$s]=fixture();throws(fn()=>$s->resume(),DomainException::class);});
test('wizard revision prevents overwriting a stale form',function(){[$s,$r,$c,$totp,$box,$g]=configured();$result=$s->saveConfiguration($g,config(),0);check($result['revision']===1);check($result['executable']===false);check($s->progress($g)['phase']==='REVIEWED');throws(fn()=>$s->saveConfiguration($g,config(),0),DomainException::class);check($s->saveConfiguration($g,config(),1)['revision']===2);});
test('configuration rejects cookie-shared hosts and conflicting ports',function(){foreach(['ports','hosts','unknown','module','shell','user-only'] as $case){$cfg=config();switch($case){case 'ports':$cfg['user_port']=8447;break;case 'hosts':$cfg['user_host']=$cfg['admin_host'];break;case 'unknown':$cfg['command']='id';break;case 'module':$cfg['modules']=['arbitrary'];break;case 'shell':$cfg['webstack']='nginx;id';break;case 'user-only':$cfg['admin_host']='';break;}throws(fn()=>Configuration::validate($cfg),InvalidArgumentException::class);}});
test('all five webstack profiles validate at the contract level',function(){foreach(Configuration::PROFILES as $profile){$cfg=config();$cfg['webstack']=$profile;check(Configuration::validate($cfg)['webstack']===$profile);}});
test('local status contains no credential material',function(){[$s,$r,$c,$totp,$box,$g,$t]=registered();$status=json_encode($s->status());check(!str_contains($status,$g));check(!str_contains($status,$t));check($s->status()['production_ready']===false);});
test('secretbox detects modification and wrong keys',function(){$box=new SecretBox(base64_encode(random_bytes(32)));$sealed=$box->encrypt('sensitive');check($box->decrypt($sealed)==='sensitive');$raw=base64_decode(substr($sealed,3));$raw[30]=chr(ord($raw[30])^1);throws(fn()=>$box->decrypt('v1:'.base64_encode($raw)));$other=new SecretBox(base64_encode(random_bytes(32)));throws(fn()=>$other->decrypt($sealed));throws(fn()=>new SecretBox('wrong'));});
test('base32 round-trips random secrets',function(){for($n=1;$n<65;$n++){$b=random_bytes($n);check(Totp::decode(Totp::encode($b))===$b);}throws(fn()=>Totp::decode('invalid!'),InvalidArgumentException::class);});
foreach([59=>'94287082',1111111109=>'07081804',1111111111=>'14050471',1234567890=>'89005924',2000000000=>'69279037',20000000000=>'65353130'] as $time=>$expected){test('RFC6238 SHA1 vector '.$time,function()use($time,$expected){$totp=new Totp();check($totp->code(Totp::encode('12345678901234567890'),$time,8)===$expected);});}
test('TOTP checks window, format and replay enrollment state',function(){$totp=new Totp();$s=$totp->newSecret();$now=1234567890;check($totp->match($s,$totp->code($s,$now),$now)===intdiv($now,30));check($totp->match($s,$totp->code($s,$now+30),$now)!==null);check($totp->match($s,'12345',$now)===null);check($totp->match($s,'abcdef',$now)===null);});
$failed=0;foreach($tests as $name=>$fn){try{$fn();echo "PASS $name\n";}catch(Throwable $e){$failed++;fwrite(STDERR,"FAIL $name: ".$e->getMessage()."\n");}}
echo count($tests)." tests, $assertions assertions, $failed failures\n";
exit($failed===0?0:1);
