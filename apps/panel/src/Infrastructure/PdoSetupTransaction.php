<?php
declare(strict_types=1);
namespace ForgePanel\Infrastructure;
use ForgePanel\Setup\SetupTransaction;
final class PdoSetupTransaction extends SetupTransaction {
    public function __construct(array $state, private \PDO $pdo) { parent::__construct($state); }
    public function hasInitialAdmin(): bool { return (int)$this->pdo->query('SELECT COUNT(*) FROM fp_admins WHERE initial_admin')->fetchColumn()>0; }
    public function createAdmin(string $id,string $email,string $hash,string $encryptedSecret):void {
        $s=$this->pdo->prepare('INSERT INTO fp_admins (id,email,password_hash,mfa_secret,initial_admin) VALUES (:id,:email,:hash,:secret,true)');
        $s->execute(['id'=>$id,'email'=>$email,'hash'=>$hash,'secret'=>$encryptedSecret]);
    }
    public function admin(string $id):array {
        $s=$this->pdo->prepare('SELECT id,email,mfa_secret,mfa_enabled FROM fp_admins WHERE id=:id');$s->execute(['id'=>$id]);
        $a=$s->fetch(\PDO::FETCH_ASSOC);if(!$a){throw new \RuntimeException('Missing initial administrator.');}
        $a['mfa_enabled']=in_array($a['mfa_enabled'],[true,1,'1','t'],true);return $a;
    }
    public function enableMfa(string $id,int $counter,array $recoveryHashes):void {
        $s=$this->pdo->prepare('UPDATE fp_admins SET mfa_enabled=true, last_totp_counter=:counter, recovery_hashes=CAST(:hashes AS jsonb) WHERE id=:id');
        $s->execute(['id'=>$id,'counter'=>$counter,'hashes'=>json_encode($recoveryHashes,JSON_THROW_ON_ERROR)]);
        if($s->rowCount()!==1){throw new \RuntimeException('Administrator MFA update failed.');}
    }
    public function disableMfa(string $id): void {
        $s=$this->pdo->prepare("UPDATE fp_admins SET mfa_enabled=false, mfa_secret=NULL, last_totp_counter=NULL, recovery_hashes='[]'::jsonb WHERE id=:id");
        $s->execute(['id'=>$id]);
        if ($s->rowCount()!==1) { throw new \RuntimeException('Administrator MFA skip failed.'); }
    }
    public function audit(string $event,array $metadata=[]):void {
        $s=$this->pdo->prepare('INSERT INTO fp_setup_audit(event,metadata) VALUES (:event,CAST(:metadata AS jsonb))');
        $s->execute(['event'=>$event,'metadata'=>json_encode($metadata,JSON_THROW_ON_ERROR)]);
    }
}
