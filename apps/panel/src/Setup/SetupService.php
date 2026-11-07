<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
final class SetupService {
    public function __construct(private SetupRepository $repo, private SecretBox $box, private Totp $totp, private Clock $clock) {}
    private static function secret(): string { return rtrim(strtr(base64_encode(random_bytes(32)), '+/', '-_'), '='); }
    private static function uuid(): string {
        $b=random_bytes(16); $b[6]=chr((ord($b[6])&15)|64); $b[8]=chr((ord($b[8])&63)|128);
        $h=bin2hex($b); return substr($h,0,8).'-'.substr($h,8,4).'-'.substr($h,12,4).'-'.substr($h,16,4).'-'.substr($h,20);
    }
    public function issue(): string {
        return $this->repo->transaction(function (SetupTransaction $tx): string {
            if ($tx->state['admin_id']!==null || $tx->hasInitialAdmin()) { throw new \DomainException('Initial administrator already exists; use local setup resume.'); }
            $token=self::secret();
            $tx->state['phase']='TOKEN_ISSUED'; $tx->state['token_hash']=hash('sha256',$token);
            $tx->state['token_expiry']=$this->clock->now()+900; $tx->state['attempts']=0;
            $tx->audit('setup.token_issued'); return $token;
        });
    }
    /** No token is consumed unless the administrator and setup capability commit. */
    public function register(string $token, string $email, string $password): array {
        $email=strtolower(trim($email));
        if (strlen($email)>254 || !filter_var($email,FILTER_VALIDATE_EMAIL) || preg_match('/[^\x20-\x7e]/',$email)) { throw new \InvalidArgumentException('Invalid ASCII email address.'); }
        if (strlen($password)<15 || strlen($password)>128 || str_contains($password,"\0")) { throw new \InvalidArgumentException('Password must contain 15..128 bytes and no NUL.'); }
        return $this->repo->transaction(function (SetupTransaction $tx) use ($token,$email,$password): array {
            $s=&$tx->state;
            if ($s['phase']!=='TOKEN_ISSUED' || $s['admin_id']!==null || $tx->hasInitialAdmin()
                || $this->clock->now()>=$s['token_expiry'] || $s['attempts']>=5) { return ['ok'=>false,'code'=>'INVALID_OR_EXPIRED']; }
            if (strlen($token)!==43 || !hash_equals((string)$s['token_hash'],hash('sha256',$token))) {
                $s['attempts']++; $tx->audit('setup.token_rejected'); return ['ok'=>false,'code'=>'INVALID_OR_EXPIRED'];
            }
            if (!in_array('argon2id',password_algos(),true)) { throw new \RuntimeException('Argon2id is required; no silent downgrade.'); }
            $hash=password_hash($password,PASSWORD_ARGON2ID,['memory_cost'=>65536,'time_cost'=>3,'threads'=>1]);
            $id=self::uuid(); $grant=self::secret(); $secret=$this->totp->newSecret();
            $tx->createAdmin($id,$email,$hash,$this->box->encrypt($secret));
            $s['admin_id']=$id; $s['phase']='MFA_PENDING'; $s['token_hash']=null; $s['token_expiry']=0;
            $s['grant_hash']=hash('sha256',$grant); $s['grant_expiry']=$this->clock->now()+1800;
            $tx->audit('setup.initial_admin_created',['admin_id'=>$id]);
            return ['ok'=>true,'grant'=>$grant];
        });
    }
    private function authorize(SetupTransaction $tx,string $grant): void {
        if (strlen($grant)!==43 || $tx->state['grant_hash']===null || $tx->state['admin_id']===null
            || $this->clock->now()>=$tx->state['grant_expiry']
            || !hash_equals($tx->state['grant_hash'],hash('sha256',$grant))) { throw new \DomainException('Setup authorization required or expired.'); }
    }
    public function enrollment(string $grant): array {
        return $this->repo->transaction(function(SetupTransaction $tx)use($grant):array {
            $this->authorize($tx,$grant);
            if ($tx->state['phase']!=='MFA_PENDING') { throw new \DomainException('MFA enrollment is not available.'); }
            $a=$tx->admin($tx->state['admin_id']);
            return ['email'=>$a['email'],'secret'=>$this->box->decrypt($a['mfa_secret'])];
        });
    }
    public function confirmMfa(string $grant,string $code): array {
        return $this->repo->transaction(function(SetupTransaction $tx)use($grant,$code):array {
            $this->authorize($tx,$grant); $s=&$tx->state;
            if ($s['phase']!=='MFA_PENDING' || $s['mfa_attempts']>=5) { return ['ok'=>false]; }
            $a=$tx->admin($s['admin_id']);
            $counter=$this->totp->match($this->box->decrypt($a['mfa_secret']),$code,$this->clock->now());
            if ($counter===null) { $s['mfa_attempts']++; $tx->audit('setup.mfa_rejected'); return ['ok'=>false]; }
            $codes=[]; for($i=0;$i<10;$i++) { $codes[]=bin2hex(random_bytes(12)); }
            $tx->enableMfa($s['admin_id'],$counter,array_map(fn(string $v):string=>hash('sha256',$v),$codes));
            $s['phase']='CONFIGURING'; $tx->audit('setup.mfa_enabled',['admin_id'=>$s['admin_id']]);
            return ['ok'=>true,'recovery_codes'=>$codes];
        });
    }
    /** Local privileged command only. Issues a one-use recovery code and revokes old setup grants. */
    public function resume(): string {
        return $this->repo->transaction(function(SetupTransaction $tx):string {
            if ($tx->state['admin_id']===null || !in_array($tx->state['phase'],['MFA_PENDING','CONFIGURING','REVIEWED'],true)) { throw new \DomainException('There is no resumable setup.'); }
            $code=self::secret();
            $tx->state['resume_hash']=hash('sha256',$code); $tx->state['resume_expiry']=$this->clock->now()+900;
            $tx->state['resume_attempts']=0; $tx->state['grant_hash']=null; $tx->state['grant_expiry']=0;
            $tx->audit('setup.local_resume_issued'); return $code;
        });
    }
    public function redeemResume(string $code): array {
        return $this->repo->transaction(function(SetupTransaction $tx)use($code):array {
            $s=&$tx->state;
            if ($s['resume_hash']===null || $s['admin_id']===null || $s['resume_attempts']>=5
                || $this->clock->now()>=$s['resume_expiry']) { return ['ok'=>false]; }
            if (strlen($code)!==43 || !hash_equals($s['resume_hash'],hash('sha256',$code))) {
                $s['resume_attempts']++; $tx->audit('setup.resume_rejected'); return ['ok'=>false];
            }
            $grant=self::secret(); $s['grant_hash']=hash('sha256',$grant); $s['grant_expiry']=$this->clock->now()+1800;
            $s['resume_hash']=null; $s['resume_expiry']=0; $s['mfa_attempts']=0;
            $tx->audit('setup.resume_redeemed'); return ['ok'=>true,'grant'=>$grant,'phase'=>$s['phase']];
        });
    }
    public function progress(string $grant): array {
        return $this->repo->transaction(function(SetupTransaction $tx)use($grant):array {
            $this->authorize($tx,$grant);
            return ['phase'=>$tx->state['phase'],'revision'=>$tx->state['config_revision'],'config'=>$tx->state['config']];
        });
    }
    public function saveConfiguration(string $grant,array $data,int $expectedRevision): array {
        $data=Configuration::validate($data);
        return $this->repo->transaction(function(SetupTransaction $tx)use($grant,$data,$expectedRevision):array {
            $this->authorize($tx,$grant); $s=&$tx->state;
            if (!in_array($s['phase'],['CONFIGURING','REVIEWED'],true) || !$tx->admin($s['admin_id'])['mfa_enabled']) { throw new \DomainException('MFA must be enrolled before configuring the server.'); }
            if ($s['config_revision']!==$expectedRevision) { throw new \DomainException('Configuration revision conflict; reload the form.'); }
            $s['config']=$data; $s['config_revision']++; $s['phase']='REVIEWED';
            $tx->audit('setup.configuration_saved',['revision'=>$s['config_revision']]);
            return ['revision'=>$s['config_revision'],'executable'=>false,'blocker'=>'production_installer_not_implemented'];
        });
    }
    public function status(): array {
        return $this->repo->transaction(fn(SetupTransaction $tx):array=>[
            'phase'=>$tx->state['phase'], 'token_expires_at'=>$tx->state['token_expiry'],
            'failed_attempts'=>$tx->state['attempts'], 'configuration_revision'=>$tx->state['config_revision'],
            'production_ready'=>false]);
    }
}
