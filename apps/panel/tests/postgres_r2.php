<?php
declare(strict_types=1);
/**
 * Real PostgreSQL R2 integration tests; no Symfony HTTP or production apply.
 * Runs ONLY on a dedicated *_test database with explicit schema-creation consent.
 * All objects are created in one random test schema and removed afterwards.
 */
require __DIR__.'/bootstrap.php';

use ForgePanel\Infrastructure\{PdoFactory, PdoSetupRepository};
use ForgePanel\Setup\{SecretBox, SetupService, SystemClock, Totp};

$dsn = getenv('FORGE_TEST_PG_DSN');
if (!is_string($dsn) || !str_starts_with($dsn, 'pgsql:')
    || getenv('FORGE_TEST_ALLOW_SCHEMA_CREATE') !== '1'
    || !extension_loaded('pdo_pgsql')) {
    fwrite(STDERR, "SKIP: real PostgreSQL, pdo_pgsql and explicit test-schema consent required.\n");
    exit(77);
}
$user = getenv('FORGE_TEST_DB_USER') ?: 'forgepanel_test';
$password = getenv('FORGE_TEST_DB_PASSWORD') ?: '';
$first = PdoFactory::create($dsn, $user, $password);
$database = (string)$first->query('SELECT current_database()')->fetchColumn();
if (!str_ends_with($database, '_test')) {
    throw new RuntimeException('Refusing to execute integration DDL outside a *_test database.');
}
$second = PdoFactory::create($dsn, $user, $password);
$secondDatabase = (string)$second->query('SELECT current_database()')->fetchColumn();
if ($database !== $secondDatabase) {
    throw new RuntimeException('Both test sessions must use the same dedicated database.');
}
$schema = 'fp_r2_'.bin2hex(random_bytes(8));
$checks = 0;
$assert = static function (bool $ok, string $message) use (&$checks): void {
    ++$checks;
    if (!$ok) {
        throw new RuntimeException('R2 PostgreSQL integration assertion failed: '.$message);
    }
};
$first->exec('CREATE SCHEMA "'.$schema.'"');
try {
    foreach ([$first, $second] as $connection) {
        $connection->exec('SET search_path TO "'.$schema.'"');
    }
    $first->beginTransaction();
    try {
        $first->exec(file_get_contents(dirname(__DIR__).'/migrations/001_setup.sql'));
        $first->exec(file_get_contents(dirname(__DIR__).'/migrations/002_optional_admin_mfa.sql'));
        $first->commit();
    } catch (Throwable $e) {
        if ($first->inTransaction()) {
            $first->rollBack();
        }
        throw $e;
    }

    $nullable = $first->prepare('SELECT is_nullable FROM information_schema.columns WHERE table_schema=:schema AND table_name=:table AND column_name=:column');
    $nullable->execute(['schema' => $schema, 'table' => 'fp_admins', 'column' => 'mfa_secret']);
    $assert($nullable->fetchColumn() === 'YES', 'optional-MFA migration did not permit NULL');
    $assert((int)$first->query('SELECT count(*) FROM fp_setup')->fetchColumn() === 1, 'setup singleton missing');

    $key = base64_encode(random_bytes(32));
    $service = new SetupService(new PdoSetupRepository($second), new SecretBox($key), new Totp(), new SystemClock());
    $observer = new SetupService(new PdoSetupRepository($first), new SecretBox($key), new Totp(), new SystemClock());
    $token = $service->issue();
    $assert(!$service->register('wrong', 'owner@example.test', 'A long temporary test passphrase!')['ok'], 'invalid proof accepted');
    $assert($observer->status()['failed_attempts'] === 1, 'invalid proof attempt was not committed across connections');

    // Another connection locks the singleton while the registration tries to use it.
    // The repository has a bounded lock timeout and must roll its SQL transaction back.
    $first->beginTransaction();
    $first->query('SELECT payload FROM fp_setup WHERE singleton=1 FOR UPDATE')->fetchColumn();
    $timedOut = false;
    try {
        $service->register($token, 'owner@example.test', 'A long temporary test passphrase!');
    } catch (PDOException $e) {
        $timedOut = $e->getCode() === '55P03';
    } finally {
        $first->rollBack();
    }
    $assert($timedOut, 'a conflicting transaction did not fail with a bounded lock timeout');
    $assert(!$second->inTransaction(), 'timed-out registration left a transaction open');
    $assert((int)$first->query('SELECT count(*) FROM fp_admins')->fetchColumn() === 0, 'blocked registration wrote an administrator');
    $assert($observer->status()['phase'] === 'TOKEN_ISSUED', 'blocked registration consumed its token');

    $registered = $service->register($token, 'owner@example.test', 'A long temporary test passphrase!');
    $assert($registered['ok'] === true, 'valid registration failed after releasing the lock');
    $grant = $registered['grant'];
    $assert(!$service->register($token, 'second@example.test', 'A different test passphrase!')['ok'], 'committed bootstrap token was replayable');
    $assert((int)$first->query('SELECT count(*) FROM fp_admins WHERE initial_admin')->fetchColumn() === 1, 'initial admin uniqueness not enforced');
    $secret = $first->query('SELECT mfa_secret FROM fp_admins WHERE initial_admin')->fetchColumn();
    $assert(is_string($secret) && $secret !== '', 'initial pending MFA secret missing');
    $service->skipMfa($grant);
    $admin = $first->query('SELECT mfa_secret, mfa_enabled, recovery_hashes::text AS recovery FROM fp_admins WHERE initial_admin')->fetch(PDO::FETCH_ASSOC);
    $assert($admin['mfa_secret'] === null, 'MFA skip retained the secret');
    $assert(!in_array($admin['mfa_enabled'], [true, 't', 1, '1'], true), 'MFA skip enabled authentication');
    $assert(json_decode($admin['recovery'], true, 8, JSON_THROW_ON_ERROR) === [], 'MFA skip retained recovery hashes');
    $assert((int)$first->query("SELECT count(*) FROM fp_setup_audit WHERE event='setup.mfa_skipped'")->fetchColumn() === 1, 'skip audit missing');

    // Test the database uniqueness independently of the service's state guard.
    $duplicateRejected = false;
    try {
        $first->exec("INSERT INTO fp_admins(id, email, password_hash, mfa_secret, initial_admin) VALUES ('11111111-1111-4111-8111-111111111111', 'other@example.test', 'not-a-real-hash', NULL, true)");
    } catch (PDOException $e) {
        $duplicateRejected = $e->getCode() === '23505';
    }
    $assert($duplicateRejected, 'database accepted a second initial administrator');

    $config = [
        'schema_version' => 1,
        'admin_port' => 8447, 'user_port' => 8446,
        'admin_host' => 'forge.example.test', 'user_host' => 'panel.example.test',
        'webstack' => 'nginx_fpm', 'modules' => [],
    ];
    $result = $service->saveConfiguration($grant, $config, 0);
    $assert($result['revision'] === 1 && $result['executable'] === false, 'reviewed plan became executable');
    $resume = $service->resume();
    $newGrant = $observer->redeemResume($resume);
    $assert($newGrant['ok'] === true, 'local resume failed across connections');
    $oldRejected = false;
    try {
        $service->progress($grant);
    } catch (DomainException) {
        $oldRejected = true;
    }
    $assert($oldRejected, 'previous setup grant survived local resume');
    $assert($observer->progress($newGrant['grant'])['revision'] === 1, 'revision not durable across connections');
    $staleRejected = false;
    try {
        $observer->saveConfiguration($newGrant['grant'], $config, 0);
    } catch (DomainException) {
        $staleRejected = true;
    }
    $assert($staleRejected, 'stale revision overwrite accepted');
    $assert((int)$first->query('SELECT count(*) FROM fp_admins')->fetchColumn() === 1, 'a second administrator was created');

    echo "PASS R2 PostgreSQL integration: {$checks} assertions, real two-session row lock, unique admin, optional MFA, audit, recovery and revision.\n";
    echo "LIMIT: no Symfony HTTP, permanent login, production migrations, VM or end-to-end hosting validated.\n";
} finally {
    foreach ([$first, $second] as $connection) {
        if ($connection->inTransaction()) {
            $connection->rollBack();
        }
        $connection->exec('SET search_path TO public');
    }
    $second = null;
    $first->exec('DROP SCHEMA IF EXISTS "'.$schema.'" CASCADE');
}