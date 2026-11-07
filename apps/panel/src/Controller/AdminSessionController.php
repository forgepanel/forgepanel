<?php
declare(strict_types=1);
namespace ForgePanel\Controller;

use ForgePanel\Identity\AdminAuthentication;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\HttpFoundation\{Request, Response};
use Symfony\Component\RateLimiter\RateLimiterFactory;
use Symfony\Component\Routing\Attribute\Route;

/** Read-only pre-install administrator shell: no system operations. */
final class AdminSessionController extends AbstractController
{
    private const MAX_SESSION_AGE_SECONDS = 1800; // Candidate TTL; security review required.

    public function __construct(
        private AdminAuthentication $identity,
        #[Autowire(service: 'limiter.admin_login_ip')] private RateLimiterFactory $ipLimiter,
        #[Autowire(service: 'limiter.admin_login_identity')] private RateLimiterFactory $identityLimiter,
    ) {}

    #[Route('/login', name: 'admin_login', methods: ['GET', 'POST'])]
    public function login(Request $request): Response
    {
        if (!$request->isMethod('POST')) {
            return $this->render('auth/login.html.twig', ['error' => null]);
        }
        $email = (string)$request->request->get('email', '');
        $clientIp = $request->getClientIp() ?? 'unknown';
        // No trusted X-Forwarded-For proxy is enabled. The account key is hashed.
        $ipAccepted = $this->ipLimiter->create($clientIp)->consume(1)->isAccepted();
        $accountAccepted = $this->identityLimiter->create(hash('sha256', strtolower(trim($email)).'|'.$clientIp))->consume(1)->isAccepted();
        if (!$ipAccepted || !$accountAccepted) {
            return new Response('Too many sign-in attempts.', 429);
        }
        if (!$this->isCsrfTokenValid('admin-login', (string)$request->request->get('_token', ''))) {
            return new Response('Invalid sign-in request.', 403);
        }
        try {
            $result = $this->identity->authenticate(
                $email,
                (string)$request->request->get('password', ''),
                (string)$request->request->get('verification', ''),
            );
        } catch (\Throwable $e) {
            error_log('ForgePanel PANEL authentication infrastructure failure: '.$e::class);
            return new Response('Sign-in is temporarily unavailable.', 503);
        }
        if ($result === null) {
            return $this->render('auth/login.html.twig', [
                'error' => 'Invalid credentials or verification code.',
            ], new Response('', 401));
        }
        // Old setup_grant and previous session credentials never cross this boundary.
        $session = $request->getSession();
        $session->migrate(true);
        $session->clear();
        $session->set('forge_admin_id', $result['id']);
        $session->set('forge_admin_seal', $result['seal']);
        $session->set('forge_admin_at', time());
        return $this->redirectToRoute('admin_readonly', [], 303);
    }

    #[Route('/admin', name: 'admin_readonly', methods: ['GET'])]
    public function readonly(Request $request): Response
    {
        $session = $request->getSession();
        $id = $session->get('forge_admin_id');
        $seal = $session->get('forge_admin_seal');
        $issuedAt = $session->get('forge_admin_at');
        if (!is_string($id) || !is_string($seal) || !is_int($issuedAt)
            || $issuedAt > time() || time() - $issuedAt >= self::MAX_SESSION_AGE_SECONDS) {
            $this->clearAdminSession($request);
            return new Response('Administrator sign-in required.', 401);
        }
        try {
            $current = $this->identity->current($id, $seal);
        } catch (\Throwable $e) {
            error_log('ForgePanel PANEL session check infrastructure failure: '.$e::class);
            return new Response('Administrator session validation unavailable.', 503);
        }
        if ($current === null) {
            $this->clearAdminSession($request);
            return new Response('Administrator sign-in required.', 401);
        }
        return $this->render('auth/readonly.html.twig', ['admin_email' => $current['email']]);
    }

    #[Route('/logout', name: 'admin_logout', methods: ['POST'])]
    public function logout(Request $request): Response
    {
        if (!$this->isCsrfTokenValid('admin-logout', (string)$request->request->get('_token', ''))) {
            return new Response('Invalid sign-out request.', 403);
        }
        $id = $request->getSession()->get('forge_admin_id');
        // A failed audit cannot leave a user logged in.
        $request->getSession()->invalidate();
        if (is_string($id)) {
            try {
                $this->identity->auditLogout($id);
            } catch (\Throwable $e) {
                error_log('ForgePanel PANEL logout audit unavailable: '.$e::class);
            }
        }
        return $this->redirectToRoute('admin_login', [], 303);
    }

    private function clearAdminSession(Request $request): void
    {
        $session = $request->getSession();
        foreach (['forge_admin_id', 'forge_admin_seal', 'forge_admin_at'] as $key) {
            $session->remove($key);
        }
    }
}
