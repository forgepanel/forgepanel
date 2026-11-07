<?php
declare(strict_types=1);
/** Symfony HttpKernel + real PostgreSQL session integration. Not a TLS browser or host install. */
use ForgePanel\Infrastructure\{PdoFactory, PdoSetupRepository};
use ForgePanel\Kernel;
use ForgePanel\Setup\{SecretBox, SetupService, SystemClock, Totp};
use Symfony\Component\HttpFoundation\{Request, Response};
use Symfony\Component\HttpFoundation\Session\{Session, Storage\MockArraySessionStorage};

require dirname(__DIR__).'/vendor/autoload.php';
require dirname(__DIR__).'/config/bootstrap.php';
$origin = (string)getenv('PANEL_ORIGIN');
$dsn = getenv('FORGE_TEST_PG_DSN');
if (getenv('APP_ENV') !== 'test' || $origin !== 'https://forge.example.test:8447'
    || getenv('FORGE_TEST_ALLOW_SCHEMA_CREATE') !== '1' || !extension_loaded('pdo_pgsql')
    || !is_string($dsn) || !str_starts_with($dsn, 'pgsql:')) {
    fwrite(STDERR, "SKIP: explicit isolated test origin and PostgreSQL setup required.\n"); exit(77);
}
$pdo = PdoFactory::create($dsn, getenv('FORGE_TEST_DB_USER') ?: 'forgepanel_test', getenv('FORGE_TEST_DB_PASSWORD') ?: '');
$database = (string)$pdo->query('SELECT current_database()')->fetchColumn();
if (!str_ends_with($database, '_test')) { throw new RuntimeException('Refusing non-test PostgreSQL database'); }
$schema = 'fp_auth_http_'.bin2hex(random_bytes(8));
$assertions = 0;
$assert = static function(bool $ok,string $message)use(&$assertions):void { ++$assertions; if(!$ok){throw new RuntimeException('R2 HTTP administrator assertion: '.$message);} };
$pdo->exec('CREATE SCHEMA "'.$schema.'"');
$kernel = null;
try {
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
    $box = new SecretBox((string)getenv('FORGE_ENCRYPTION_KEY'));
    $setup = new SetupService(new PdoSetupRepository($pdo), $box, new Totp(), new SystemClock());
    $token = $setup->issue();
    $password = 'A long unique password for the R2 HTTP test!';
    $registered = $setup->register($token, 'owner@example.test', $password);
    $assert($registered['ok'] === true, 'initial registration not persisted');
    $setup->skipMfa($registered['grant']);
    $setup->saveConfiguration($registered['grant'], ['schema_version'=>1,'admin_port'=>8447,'user_port'=>8446,'admin_host'=>'forge.example.test','user_host'=>'panel.example.test','webstack'=>'nginx_fpm','modules'=>[]], 0);

    // PGOPTIONS affects only new libpq sessions, keeping the Symfony PDO inside
    // this random schema while refusing to modify any other instance/database.
    putenv('PGOPTIONS=-c search_path='.$schema);
    $kernel = new Kernel('test', false);
    $session = new Session(new MockArraySessionStorage());
    $dispatch = static function(string $method,string $path,array $form=[],array $server=[])use($kernel,$session,$origin):Response{
        $request = Request::create($origin.$path, $method, $form, [], [], array_merge(['REMOTE_ADDR'=>'127.0.0.1'], $server));
        $request->setSession($session);
        $response = $kernel->handle($request);
        $kernel->terminate($request, $response);
        return $response;
    };
    $form = $dispatch('GET', '/login');
    $assert($form->getStatusCode() === 200, 'login form was not rendered');
    $content = (string)$form->getContent();
    $assert(str_contains($content, 'name="password"') && str_contains($content, 'name="verification"'), 'login form omitted credentials/MFA');
    $assert(preg_match('/name="_token" value="([^"]+)"/', $content, $matches) === 1, 'login CSRF token missing');
    $csrf = $matches[1];
    $assert($dispatch('GET', '/admin')->getStatusCode() === 401, 'anonymous read-only admin accepted');
    $assert($dispatch('POST', '/login', ['email'=>'owner@example.test','password'=>$password])->getStatusCode() === 403, 'missing CSRF accepted');
    $assert($dispatch('POST', '/login', ['_token'=>$csrf,'email'=>'unknown@example.test','password'=>'wrong'])->getStatusCode() === 401, 'unknown account enumeration');
    $assert($dispatch('POST', '/login', ['_token'=>$csrf,'email'=>'owner@example.test','password'=>'wrong'])->getStatusCode() === 401, 'wrong admin password accepted');
    $idBefore = $session->getId();
    $success = $dispatch('POST', '/login', ['_token'=>$csrf,'email'=>'owner@example.test','password'=>$password]);
    $assert($success->getStatusCode() === 303, 'correct read-only login failed');
    $assert($session->getId() !== $idBefore, 'login did not rotate session identifier');
    $assert(!$session->has('setup_grant'), 'setup grant carried into permanent login');
    $authorized = $dispatch('GET', '/admin');
    $assert($authorized->getStatusCode() === 200, 'authenticated admin preview inaccessible');
    $assert(str_contains((string)$authorized->getContent(), 'NOT installed'), 'read-only not-installed warning missing');
    $assert(!str_contains((string)$authorized->getContent(), $password), 'password rendered in admin view');
    $assert($dispatch('POST', '/admin')->getStatusCode() === 405, 'read-only admin accepted mutation');
    $assert($dispatch('GET', '/logout')->getStatusCode() === 405, 'logout accepted GET');
    $assert($dispatch('POST', '/login', ['_token'=>$csrf,'email'=>'owner@example.test','password'=>$password], ['HTTP_ORIGIN'=>'https://attacker.example.test'])->getStatusCode() === 403, 'cross-origin login POST accepted');
    $assert($dispatch('POST', '/logout')->getStatusCode() === 403, 'logout missing CSRF accepted');
    $assert(preg_match('/name="_token" value="([^"]+)"/', (string)$authorized->getContent(), $logoutMatches) === 1, 'logout CSRF token missing');
    $assert($dispatch('POST', '/logout', ['_token'=>$logoutMatches[1]])->getStatusCode() === 303, 'logout failed');
    $assert($dispatch('GET', '/admin')->getStatusCode() === 401, 'logout did not revoke session');
    $assert((int)$pdo->query("SELECT count(*) FROM fp_setup_audit WHERE event='auth.login_succeeded'")->fetchColumn() === 1, 'login audit missing');
    $assert((int)$pdo->query("SELECT count(*) FROM fp_setup_audit WHERE event='auth.logout'")->fetchColumn() === 1, 'logout audit missing');
    $loginAgain = $dispatch('GET', '/login');
    $assert(preg_match('/name="_token" value="([^"]+)"/', (string)$loginAgain->getContent(), $nextLogin) === 1, 'second login missing CSRF');
    $assert($dispatch('POST', '/login', ['_token'=>$nextLogin[1],'email'=>'owner@example.test','password'=>$password])->getStatusCode() === 303, 'new login after logout denied');
    $session->set('forge_admin_at', time()-1900);
    $assert($dispatch('GET', '/admin')->getStatusCode() === 401, 'expired admin session accepted');
    $assert(!$session->has('forge_admin_id'), 'expired session principal remained');
    $thirdForm = $dispatch('GET', '/login');
    $assert(preg_match('/name="_token" value="([^"]+)"/', (string)$thirdForm->getContent(), $thirdToken) === 1, 'third login missing CSRF');
    $assert($dispatch('POST', '/login', ['_token'=>$thirdToken[1],'email'=>'owner@example.test','password'=>$password])->getStatusCode() === 303, 'login after expiry denied');
    $session->set('forge_admin_seal', str_repeat('0', 64));
    $assert($dispatch('GET', '/admin')->getStatusCode() === 401, 'forged session seal accepted');
    $assert(!$session->has('forge_admin_id'), 'forged session principal remained');
    echo "PASS R2 Symfony admin HTTP with real PostgreSQL: {$assertions} assertions (CSRF, password, session rotation, read-only authorization, logout).\n";
    echo "LIMIT: MockArraySessionStorage, not an actual browser/cookie/TLS gateway, no panel host privileges or finished production authentication.\n";
} finally {
    if ($kernel !== null) { $kernel->shutdown(); }
    putenv('PGOPTIONS');
    if ($pdo->inTransaction()) { $pdo->rollBack(); }
    $pdo->exec('SET search_path TO public');
    $pdo->exec('DROP SCHEMA IF EXISTS "'.$schema.'" CASCADE');
}
