<?php
declare(strict_types=1);
namespace ForgePanel\Identity;

use ForgePanel\Setup\{Clock, SecretBox, Totp};

/**
 * Permanent PANEL identity for the read-only, uninstalled R2 shell.
 * No Linux, hosting, Hub or authorization-to-apply capabilities are issued here.
 */
final class AdminAuthentication
{
    // Non-secret dummy Argon2id verifier prevents immediate account enumeration.
    private const DUMMY_HASH = '$argon2id$v=19$m=65536,t=3,p=1$RkFOTHozbnpvSHVRNEpxVw$emDDGpp9P2xh/+JhJfUuF+TNq/62KXRMruUvsecC+rA';

    public function __construct(
        private \PDO $pdo,
        private SecretBox $box,
        private Totp $totp,
        private Clock $clock,
        private string $sessionSealKey,
    ) {
        if (strlen($sessionSealKey) < 32) {
            throw new \RuntimeException('A distinct configured application secret is required.');
        }
    }

    /** @return array{id:string,email:string,seal:string}|null */
    public function authenticate(string $email, string $password, string $verification = ''): ?array
    {
        $email = strtolower(trim($email));
        if (strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)
            || preg_match('/[^\x20-\x7e]/', $email)) {
            $email = '';
        }
        if (strlen($password) > 128 || strlen($password) === 0 || str_contains($password, "\0")) {
            $password = '';
        }
        if (strlen($verification) > 64) {
            $verification = '';
        }

        $this->pdo->beginTransaction();
        try {
            $this->pdo->exec("SET LOCAL lock_timeout = '3s'");
            $this->pdo->exec("SET LOCAL statement_timeout = '10s'");
            $state = $this->loadState(true);
            $query = $this->pdo->prepare('SELECT id, email, password_hash, role, mfa_enabled, mfa_secret, last_totp_counter, recovery_hashes FROM fp_admins WHERE email=:email AND initial_admin=true FOR UPDATE');
            $query->execute(['email' => $email]);
            $row = $query->fetch(\PDO::FETCH_ASSOC);
            $passwordOk = password_verify($password, is_array($row) ? (string)$row['password_hash'] : self::DUMMY_HASH);
            $eligible = is_array($row) && $passwordOk && $this->eligible($row, $state);
            if ($eligible && $this->enabled($row['mfa_enabled'])) {
                $eligible = $this->consumeMfa($row, $verification);
            }
            if (!$eligible) {
                $this->audit('auth.login_rejected');
                $this->pdo->commit();
                return null;
            }
            $this->audit('auth.login_succeeded', ['admin_id' => $row['id']]);
            $this->pdo->commit();
            return ['id' => $row['id'], 'email' => $row['email'], 'seal' => $this->seal($row)];
        } catch (\Throwable $e) {
            if ($this->pdo->inTransaction()) {
                $this->pdo->rollBack();
            }
            throw $e;
        }
    }

    /** @return array{id:string,email:string}|null */
    public function current(string $id, string $seal): ?array
    {
        if (!preg_match('/\A[0-9a-f-]{36}\z/D', $id) || !preg_match('/\A[0-9a-f]{64}\z/D', $seal)) {
            return null;
        }
        $state = $this->loadState(false);
        $stmt = $this->pdo->prepare('SELECT id,email,password_hash,role,mfa_enabled FROM fp_admins WHERE id=:id AND initial_admin=true');
        $stmt->execute(['id' => $id]);
        $row = $stmt->fetch(\PDO::FETCH_ASSOC);
        if (!is_array($row) || !$this->eligible($row, $state) || !hash_equals($this->seal($row), $seal)) {
            return null;
        }
        return ['id' => $row['id'], 'email' => $row['email']];
    }

    public function auditLogout(string $id): void
    {
        if (!preg_match('/\A[0-9a-f-]{36}\z/D', $id)) {
            return;
        }
        $this->audit('auth.logout', ['admin_id' => $id]);
    }

    /** @return array<string,mixed> */
    private function loadState(bool $lock): array
    {
        $raw = $this->pdo->query('SELECT payload FROM fp_setup WHERE singleton=1'.($lock ? ' FOR SHARE' : ''))->fetchColumn();
        if (!is_string($raw)) {
            throw new \RuntimeException('Initial setup database state is missing.');
        }
        $state = json_decode($raw, true, 32, JSON_THROW_ON_ERROR);
        if (!is_array($state) || ($state['version'] ?? null) !== 1) {
            throw new \RuntimeException('Initial setup database state is unsupported.');
        }
        return $state;
    }

    /** @param array<string,mixed> $row @param array<string,mixed> $state */
    private function eligible(array $row, array $state): bool
    {
        // REVIEWED means the install plan was reviewed, NOT applied.
        return ($state['phase'] ?? null) === 'REVIEWED'
            && is_string($state['admin_id'] ?? null)
            && hash_equals($state['admin_id'], $row['id'])
            && $row['role'] === 'ROLE_SUPER_ADMIN';
    }

    private function enabled(mixed $value): bool
    {
        return in_array($value, [true, 't', 1, '1'], true);
    }

    /** @param array<string,mixed> $row */
    private function consumeMfa(array $row, string $verification): bool
    {
        if (!is_string($row['mfa_secret']) || $row['mfa_secret'] === '') {
            throw new \RuntimeException('The configured MFA state is inconsistent.');
        }
        if (preg_match('/\A[0-9]{6}\z/D', $verification)) {
            $counter = $this->totp->match($this->box->decrypt($row['mfa_secret']), $verification, $this->clock->now());
            $lastCounter = $row['last_totp_counter'] === null ? null : (int)$row['last_totp_counter'];
            if ($counter === null || ($lastCounter !== null && $counter <= $lastCounter)) {
                return false;
            }
            $stmt = $this->pdo->prepare('UPDATE fp_admins SET last_totp_counter=:counter WHERE id=:id AND mfa_enabled=true AND (last_totp_counter IS NULL OR last_totp_counter<:previous)');
            $stmt->execute(['counter' => $counter, 'previous' => $counter, 'id' => $row['id']]);
            return $stmt->rowCount() === 1;
        }
        if (!preg_match('/\A[0-9a-f]{24}\z/D', $verification)) {
            return false;
        }
        $hashes = json_decode((string)$row['recovery_hashes'], true, 16, JSON_THROW_ON_ERROR);
        if (!is_array($hashes) || count($hashes) > 20) {
            throw new \RuntimeException('Invalid administrator recovery state.');
        }
        $digest = hash('sha256', $verification);
        $match = null;
        foreach ($hashes as $index => $hash) {
            if (!is_string($hash) || !preg_match('/\A[0-9a-f]{64}\z/D', $hash)) {
                throw new \RuntimeException('Invalid administrator recovery state.');
            }
            if (hash_equals($hash, $digest)) {
                $match = $index;
            }
        }
        if ($match === null) {
            return false;
        }
        unset($hashes[$match]);
        $stmt = $this->pdo->prepare('UPDATE fp_admins SET recovery_hashes=CAST(:hashes AS jsonb) WHERE id=:id AND mfa_enabled=true');
        $stmt->execute(['hashes' => json_encode(array_values($hashes), JSON_THROW_ON_ERROR), 'id' => $row['id']]);
        return $stmt->rowCount() === 1;
    }

    /** @param array<string,mixed> $row */
    private function seal(array $row): string
    {
        $material = $row['id'].'|'.$row['role'].'|'.$row['password_hash'].'|'.($this->enabled($row['mfa_enabled']) ? 'mfa' : 'no-mfa');
        return hash_hmac('sha256', $material, $this->sessionSealKey);
    }

    /** @param array<string,mixed> $metadata */
    private function audit(string $event, array $metadata = []): void
    {
        $stmt = $this->pdo->prepare('INSERT INTO fp_setup_audit(event,metadata) VALUES (:event,CAST(:metadata AS jsonb))');
        $stmt->execute(['event' => $event, 'metadata' => json_encode($metadata, JSON_THROW_ON_ERROR)]);
    }
}
