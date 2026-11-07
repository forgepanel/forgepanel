<?php
declare(strict_types=1);
/**
 * Real Symfony HttpKernel smoke checks. No production install or persistent login.
 * Needs vendor/ resolved in a disposable test environment and test-only env vars.
 */
use ForgePanel\Kernel;
use Symfony\Component\HttpFoundation\Request;

require dirname(__DIR__).'/vendor/autoload.php';
require dirname(__DIR__).'/config/bootstrap.php';

$origin = (string)($_SERVER['PANEL_ORIGIN'] ?? $_ENV['PANEL_ORIGIN'] ?? getenv('PANEL_ORIGIN'));
if ($origin !== 'https://forge.example.test:8447') {
    throw new RuntimeException('Refusing unexpected R2 test origin.');
}
if ((string)($_SERVER['APP_ENV'] ?? $_ENV['APP_ENV'] ?? getenv('APP_ENV')) !== 'test') {
    throw new RuntimeException('R2 HTTP smoke tests require APP_ENV=test.');
}
$checks = 0;
$assert = static function (bool $ok, string $message) use (&$checks): void {
    ++$checks;
    if (!$ok) {
        throw new RuntimeException('R2 Symfony HTTP assertion failed: '.$message);
    }
};
$kernel = new Kernel('test', false);
$dispatch = static function (string $url, string $method = 'GET', array $server = [], ?string $content = null) use ($kernel): \Symfony\Component\HttpFoundation\Response {
    $request = Request::create($url, $method, [], [], [], array_merge(['REMOTE_ADDR'=>'127.0.0.1'], $server), $content);
    $response = $kernel->handle($request);
    $kernel->terminate($request, $response);
    return $response;
};
try {
    $valid = $dispatch($origin.'/setup');
    $assert($valid->getStatusCode() === 200, 'secure expected origin did not render setup form: HTTP '.$valid->getStatusCode());
    $assert(str_contains((string)$valid->getContent(), 'bootstrap_token'), 'setup template missing bootstrap input');
    $assert($valid->headers->get('X-Frame-Options') === 'DENY', 'missing anti-framing response header');
    $assert($valid->headers->get('X-Content-Type-Options') === 'nosniff', 'missing no-sniff header');
    $assert(str_contains((string)$valid->headers->get('Cache-Control'), 'no-store'), 'missing non-caching policy');

    $insecure = $dispatch('http://forge.example.test:8447/setup');
    $assert($insecure->getStatusCode() === 421, 'HTTP accepted on HTTPS-only origin');
    $wrongHost = $dispatch('https://attacker.example.test:8447/setup');
    $assert($wrongHost->getStatusCode() === 421, 'untrusted Host accepted');
    $wrongPort = $dispatch('https://forge.example.test:8446/setup');
    $assert($wrongPort->getStatusCode() === 421, 'untrusted port accepted');
    $method = $dispatch($origin.'/setup', 'PUT');
    $assert($method->getStatusCode() === 405, 'unlisted HTTP method accepted');
    $wrongOrigin = $dispatch($origin.'/setup', 'POST', ['HTTP_ORIGIN'=>'https://attacker.example.test']);
    $assert($wrongOrigin->getStatusCode() === 403, 'cross-origin POST not denied');
    $tooLarge = $dispatch($origin.'/setup', 'POST', ['HTTP_ORIGIN'=>$origin], str_repeat('x', 32769));
    $assert($tooLarge->getStatusCode() === 413, 'oversized body not rejected');
    $missingCsrf = $dispatch($origin.'/setup', 'POST', ['HTTP_ORIGIN'=>$origin]);
    // With no permanent login, the unfinished security firewall may translate
    // AccessDeniedException into 401 rather than 403; both must reject mutation.
    $assert(in_array($missingCsrf->getStatusCode(), [401, 403], true),
        'POST without CSRF unexpectedly succeeded or redirected');

    echo "PASS real Symfony HttpKernel: {$checks} assertions (setup GET, host/HTTPS/origin/port, method, size, CSRF, security headers).\n";
    echo "LIMIT: this is not a browser/E2E suite, login, production HTTPS, SQL migration or installer certification.\n";
} finally {
    $kernel->shutdown();
}