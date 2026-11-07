<?php
declare(strict_types=1);
// Live integration test. Never point this at a production database.
require __DIR__.'/bootstrap.php';
use ForgePanel\Infrastructure\{PdoFactory,PdoSetupRepository};
use ForgePanel\Setup\{SetupService,SecretBox,Totp,SystemClock};
$dsn=getenv('FORGE_TEST_PG_DSN');
if (!$dsn || getenv('FORGE_TEST_ALLOW_SCHEMA_CREATE')!=='1' || !extension_loaded('pdo_pgsql')) {
    fwrite(STDERR,"SKIP: PostgreSQL PDO, a dedicated *_test database and explicit schema permission are required.\n");exit(77);
}
$pdo=PdoFactory::create($dsn,getenv('FORGE_TEST_DB_USER')?:'forgepanel_test',getenv('FORGE_TEST_DB_PASSWORD')?:'');
$db=(string)$pdo->query('SELECT current_database()')->fetchColumn();
if (!str_ends_with($db,'_test')) { throw new RuntimeException('Refusing non-test database.'); }
$schema='fp_test_'.bin2hex(random_bytes(8));
function expect(bool $ok,string $message):void {if(!$ok){throw new RuntimeException($message);}}
try {
    $pdo->exec('CREATE SCHEMA "'.$schema.'"');
    $pdo->exec('SET search_path TO "'.$schema.'"');
    $pdo->beginTransaction();$pdo->exec(file_get_contents(dirname(__DIR__).'/migrations/001_setup.sql'));$pdo->commit();
    $service=new SetupService(new PdoSetupRepository($pdo),new SecretBox(base64_encode(random_bytes(32))),new Totp(),new SystemClock());
    $token=$service->issue();
    // Force an audit insert failure AFTER the administrator insert.
    $pdo->exec("CREATE FUNCTION fail_setup_test() RETURNS trigger LANGUAGE plpgsql AS \$\$ BEGIN IF NEW.event = 'setup.initial_admin_created' THEN RAISE EXCEPTION 'simulated transaction failure'; END IF; RETURN NEW; END; \$\$");
    $pdo->exec('CREATE TRIGGER fail_setup_test BEFORE INSERT ON fp_setup_audit FOR EACH ROW EXECUTE FUNCTION fail_setup_test()');
    $failed=false;
    try {$service->register($token,'owner@example.com','An integration test passphrase!');} catch(PDOException) {$failed=true;}
    expect($failed,'Expected simulated failure');
    expect((int)$pdo->query('SELECT COUNT(*) FROM fp_admins')->fetchColumn()===0,'Administrator insert did not roll back');
    expect($service->status()['phase']==='TOKEN_ISSUED','Token was consumed despite rollback');
    $pdo->exec('DROP TRIGGER fail_setup_test ON fp_setup_audit');
    $pdo->exec('DROP FUNCTION fail_setup_test()');
    $result=$service->register($token,'owner@example.com','An integration test passphrase!');
    expect($result['ok'],'Valid registration failed');
    expect(!$service->register($token,'other@example.com','Another test passphrase!')['ok'],'Replayed token accepted');
    expect((int)$pdo->query('SELECT COUNT(*) FROM fp_admins')->fetchColumn()===1,'Wrong initial account count');
    $e=$service->enrollment($result['grant']);
    expect($service->confirmMfa($result['grant'],(new Totp())->code($e['secret'],time()))['ok'],'MFA failed');
    $cfg=['schema_version'=>1,'admin_port'=>8447,'user_port'=>8446,'admin_host'=>'forge.example.com','user_host'=>'panel.example.com','webstack'=>'nginx_fpm','modules'=>[]];
    expect($service->saveConfiguration($result['grant'],$cfg,0)['revision']===1,'Configuration save failed');
    echo "PASS PostgreSQL schema, transaction rollback, single initial admin, MFA, configuration persistence\n";
    echo "NOTE: this smoke test does not establish concurrent registration or crash-recovery correctness.\n";
} finally {
    if($pdo->inTransaction()){$pdo->rollBack();}
    $pdo->exec('SET search_path TO public');
    $pdo->exec('DROP SCHEMA IF EXISTS "'.$schema.'" CASCADE');
}
