<?php
declare(strict_types=1);
/** SQL-backed, nonproduction administrator identity tests; disposable PostgreSQL only. */
require dirname(__DIR__).'/vendor/autoload.php';

use ForgePanel\Identity\AdminAuthentication;
use ForgePanel\Infrastructure\{PdoFactory, PdoSetupRepository};
use ForgePanel\Setup\{Clock, SecretBox, SetupService, Totp};

if (($_SERVER['APP_ENV'] ?? $_ENV['APP_ENV'] ?? getenv('APP_ENV')) !== 'test'
    || getenv('FORGE_TEST_ALLOW_SCHEMA_CREATE') !== '1'
    || !extension_loaded('pdo_pgsql') || !extension_loaded('sodium')) {
    fwrite(STDERR, "SKIP: opt-in test-only PostgreSQL environment, pdo_pgsql and sodium required.\n");
    exit(77);
}
$dsn = getenv('FORGE_TEST_PG_DSN');
if (!is_string($dsn) || !str_starts_with($dsn, 'pgsql:')) {
    fwrite(STDERR, "SKIP: explicit dedicated PostgreSQL test DSN required.\n");
    exit(77);
}
$pdo = PdoFactory::create($dsn, getenv('FORGE_TEST_DB_USER') ?: 'forgepanel_test', getenv('FORGE_TEST_DB_PASSWORD') ?: '');
$database = (string)$pdo->query('SELECT current_database()')->fetchColumn();
if (!str_ends_with($database, '_test')) {
    throw new RuntimeException('Refusing non-test database.');
}
$secretKey = (string)getenv('APP_SECRET');
if (strlen($secretKey) < 32) {
    throw new RuntimeException('Test APP_SECRET must not be empty.');
}
$box = new SecretBox(base64_encode(random_bytes(32)));
$totp = new Totp();
$clock = new class implements Clock {
    public int $time;
    public function __construct() { $this->time = time(); }
    public function now(): int { return $this->time; }
};
$assertions = 0;
$assert = static function(bool $ok,string $message)use(&$assertions):void{
    ++$assertions;
    if (!$ok) { throw new RuntimeException('R2 administrator identity assertion: '.$message); }
};
$schemas = [];
try {
    foreach (['without-mfa', 'with-mfa'] as $mode) {
        $schema = 'fp_auth_'.bin2hex(random_bytes(8));
        $pdo->exec('CREATE SCHEMA "'.$schema.'"');
        $schemas[] = $schema;
        $pdo->exec('SET search_path TO "'.$schema.'"');
        $pdo->beginTransaction();
        try {
            $pdo->exec(file_get_contents(dirname(__DIR__).'/migrations/001_setup.sql'));
            $pdo->exec(file_get_contents(dirname(__DIR__).'/migrations/002_optional_admin_mfa.sql'));
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) { $pdo->rollBack(); }
            throw $e;
        }
        $setup = new SetupService(new PdoSetupRepository($pdo), $box, $totp, $clock);
        $identity = new AdminAuthentication($pdo, $box, $totp, $clock, $secretKey);
        $token = $setup->issue();
        $assert($identity->authenticate('unknown@example.test', 'A password never used') === null, 'unknown account accepted');
        $password = 'A long and unique administrator password!';
        $result = $setup->register($token, 'OWNER@example.test', $password);
        $assert($result['ok'] === true, 'initial account registration failed');
        $grant = $result['grant'];
        $assert($identity->authenticate('owner@example.test', $password) === null, 'login was allowed before reviewed setup');
        if ($mode === 'without-mfa') {
            $setup->skipMfa($grant);
        } else {
            $enrollment = $setup->enrollment($grant);
            $confirmed = $setup->confirmMfa($grant, $totp->code($enrollment['secret'], $clock->now()));
            $assert($confirmed['ok'] === true, 'TOTP enrollment failed');
        }
        $configuration = ['schema_version'=>1,'admin_port'=>8447,'user_port'=>8446,'admin_host'=>'forge.example.test','user_host'=>'panel.example.test','webstack'=>'nginx_fpm','modules'=>[]];
        $assert($setup->saveConfiguration($grant, $configuration, 0)['executable'] === false, 'setup unexpectedly permitted system apply');
        $assert($identity->authenticate('owner@example.test', 'wrong password') === null, 'wrong password accepted');
        if ($mode === 'without-mfa') {
            $user = $identity->authenticate(' OWNER@example.test ', $password);
            $assert(is_array($user), 'correct password should work with optional MFA disabled');
            $assert($identity->current($user['id'], $user['seal']) !== null, 'valid credential fingerprint not accepted');
            $assert($identity->current($user['id'], str_repeat('0', 64)) === null, 'forged session fingerprint accepted');
            $storedHash = (string)$pdo->query('SELECT password_hash FROM fp_admins WHERE initial_admin')->fetchColumn();
            $stmt = $pdo->prepare('UPDATE fp_admins SET password_hash=:new WHERE initial_admin');
            $stmt->execute(['new'=>password_hash('Rotated and inaccessible test password', PASSWORD_ARGON2ID)]);
            $assert($identity->current($user['id'], $user['seal']) === null, 'password rotation failed to revoke session');
            $stmt->execute(['new'=>$storedHash]);
            $assert($identity->current($user['id'], $user['seal']) !== null, 'restored test credential fingerprint not accepted');
            $assert(in_array($pdo->query('SELECT mfa_secret IS NULL FROM fp_admins WHERE initial_admin')->fetchColumn(), [true, 't', '1', 1], true), 'disabled MFA retained secret');
        } else {
            $clock->time += 61; // never reuse enrollment step for first permanent login.
            $code = $totp->code($enrollment['secret'], $clock->now());
            $assert($identity->authenticate('owner@example.test', $password, '00000000') === null, 'invalid TOTP accepted');
            $user = $identity->authenticate('owner@example.test', $password, $code);
            $assert(is_array($user), 'valid TOTP denied');
            $assert($identity->authenticate('owner@example.test', $password, $code) === null, 'replayed TOTP accepted');
            $recovery = $confirmed['recovery_codes'][0];
            $assert(is_array($identity->authenticate('owner@example.test', $password, $recovery)), 'recovery code denied');
            $assert($identity->authenticate('owner@example.test', $password, $recovery) === null, 'used recovery code replay accepted');
            $hashes = (string)$pdo->query('SELECT recovery_hashes::text FROM fp_admins WHERE initial_admin')->fetchColumn();
            $assert(count(json_decode($hashes, true, 32, JSON_THROW_ON_ERROR)) === 9, 'recovery code not consumed');
            $assert($identity->current($user['id'], $user['seal']) !== null, 'valid MFA session no longer recognized');
            $pdo->exec('UPDATE fp_admins SET mfa_enabled=false WHERE initial_admin');
            $assert($identity->current($user['id'], $user['seal']) === null, 'MFA policy change failed to revoke prior session');
        }
        $audit = (int)$pdo->query("SELECT count(*) FROM fp_setup_audit WHERE event='auth.login_rejected'")->fetchColumn();
        $assert($audit >= 2, 'authentication denial was not audited');
        $json = (string)$pdo->query("SELECT coalesce(string_agg(metadata::text,' '),'') FROM fp_setup_audit WHERE event LIKE 'auth.%'")->fetchColumn();
        $assert(!str_contains($json, $password) && !str_contains($json, $token), 'credential leaked to audit');
    }
    echo "PASS R2 permanent administrator identity: {$assertions} real PostgreSQL assertions (optional MFA, TOTP anti-replay, recovery, credential/session revocation).\n";
    echo "LIMIT: read-only setup preview; no root/hosting authorization, real TLS gateway or browser E2E certified.\n";
} finally {
    if ($pdo->inTransaction()) { $pdo->rollBack(); }
    $pdo->exec('SET search_path TO public');
    foreach (array_reverse($schemas) as $schema) {
        $pdo->exec('DROP SCHEMA IF EXISTS "'.$schema.'" CASCADE');
    }
}
