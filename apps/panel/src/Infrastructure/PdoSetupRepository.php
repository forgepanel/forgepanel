<?php
declare(strict_types=1);
namespace ForgePanel\Infrastructure;
use ForgePanel\Setup\SetupRepository;
final class PdoSetupRepository implements SetupRepository {
    public function __construct(private \PDO $pdo) {}
    public function transaction(callable $operation): mixed {
        $this->pdo->beginTransaction();
        try {
            $this->pdo->exec("SET LOCAL lock_timeout = '3s'");
            $this->pdo->exec("SET LOCAL statement_timeout = '10s'");
            $raw=$this->pdo->query('SELECT payload FROM fp_setup WHERE singleton = 1 FOR UPDATE')->fetchColumn();
            if (!is_string($raw)) { throw new \RuntimeException('Setup schema must be initialized by the local installer.'); }
            $state=json_decode($raw,true,32,JSON_THROW_ON_ERROR);
            if (($state['version']??null)!==1 || array_diff(array_keys(\ForgePanel\Setup\SetupTransaction::initial()),array_keys($state))) { throw new \RuntimeException('Unsupported or corrupt setup state.'); }
            $tx=new PdoSetupTransaction($state,$this->pdo); $result=$operation($tx);
            $q=$this->pdo->prepare('UPDATE fp_setup SET payload=CAST(:payload AS jsonb) WHERE singleton=1');
            $q->execute(['payload'=>json_encode($tx->state,JSON_THROW_ON_ERROR)]);
            $this->pdo->commit(); return $result;
        } catch (\Throwable $e) {
            if ($this->pdo->inTransaction()) { $this->pdo->rollBack(); }
            throw $e;
        }
    }
}
