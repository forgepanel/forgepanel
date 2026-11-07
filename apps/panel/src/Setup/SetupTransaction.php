<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
abstract class SetupTransaction {
    public function __construct(public array $state) {}
    public static function initial(): array {
        return ['version'=>1, 'phase'=>'NEW', 'token_hash'=>null, 'token_expiry'=>0,
            'attempts'=>0, 'grant_hash'=>null, 'grant_expiry'=>0, 'admin_id'=>null,
            'mfa_attempts'=>0, 'config_revision'=>0, 'config'=>null,
            'resume_hash'=>null, 'resume_expiry'=>0, 'resume_attempts'=>0];
    }
    abstract public function hasInitialAdmin(): bool;
    abstract public function createAdmin(string $id, string $email, string $hash, string $encryptedSecret): void;
    abstract public function admin(string $id): array;
    abstract public function enableMfa(string $id, int $counter, array $recoveryHashes): void;
    abstract public function audit(string $event, array $metadata=[]): void;
}
