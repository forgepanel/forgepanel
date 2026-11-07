<?php
declare(strict_types=1);
namespace ForgePanelTests;
use ForgePanel\Setup\SetupRepository;
use ForgePanel\Setup\SetupTransaction;
final class MemoryTransaction extends SetupTransaction {
    public array $admins=[];
    public array $events=[];
    public bool $failAfterInsert=false;
    public function hasInitialAdmin():bool { return count($this->admins)>0; }
    public function createAdmin(string $id,string $email,string $hash,string $secret):void {
        if ($this->hasInitialAdmin()) { throw new \RuntimeException('Unique initial admin violation.'); }
        $this->admins[$id]=['id'=>$id,'email'=>$email,'password_hash'=>$hash,'mfa_secret'=>$secret,'mfa_enabled'=>false];
        if ($this->failAfterInsert) { throw new \RuntimeException('Simulated database write failure.'); }
    }
    public function admin(string $id):array { return $this->admins[$id]; }
    public function enableMfa(string $id,int $counter,array $hashes):void {
        $this->admins[$id]['mfa_enabled']=true;$this->admins[$id]['counter']=$counter;$this->admins[$id]['recovery_hashes']=$hashes;
    }
    public function audit(string $event,array $metadata=[]):void { $this->events[]=[$event,$metadata]; }
}
final class MemoryRepository implements SetupRepository {
    public MemoryTransaction $data;
    public function __construct() { $this->data=new MemoryTransaction(SetupTransaction::initial()); }
    public function transaction(callable $operation): mixed {
        $work=clone $this->data;
        $result=$operation($work);
        $this->data=$work;
        return $result;
    }
}
final class MutableClock implements \ForgePanel\Setup\Clock {
    public int $time=1793836800;
    public function now():int { return $this->time; }
}
