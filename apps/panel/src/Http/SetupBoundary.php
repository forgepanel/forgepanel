<?php
declare(strict_types=1);
namespace ForgePanel\Http;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\HttpKernel\Event\ResponseEvent;
use Symfony\Component\HttpFoundation\Response;
final class SetupBoundary implements EventSubscriberInterface {
    private string $origin;
    public function __construct(string $panelOrigin) {
        $p=parse_url($panelOrigin);
        if (!$p || ($p['scheme']??null)!=='https' || empty($p['host']) || isset($p['user']) || isset($p['pass'])
            || isset($p['query']) || isset($p['fragment']) || !in_array($p['path']??'',['','/'],true)) {
            throw new \RuntimeException('PANEL_ORIGIN must be an exact HTTPS origin.');
        }
        $this->origin='https://'.strtolower($p['host']).(isset($p['port']) && $p['port']!==443?':'.$p['port']:'');
    }
    public static function getSubscribedEvents():array {
        return ['kernel.request'=>['request',1000], 'kernel.response'=>['response',-1000]];
    }
    public function request(RequestEvent $event):void {
        if (!$event->isMainRequest()) { return; }
        $r=$event->getRequest();
        // No trusted proxy is configured in this release. Do not trust client-supplied forwarding headers.
        if (!$r->isSecure() || strtolower($r->getSchemeAndHttpHost())!==$this->origin) {
            $event->setResponse(new Response('Use the configured administrator HTTPS origin.',421));return;
        }
        if (!in_array($r->getMethod(),['GET','HEAD','POST'],true)) {
            $event->setResponse(new Response('Method not allowed.',405,['Allow'=>'GET, HEAD, POST']));return;
        }
        if ($r->getMethod()==='POST') {
            $origin=$r->headers->get('Origin');
            if ($origin!==null && strtolower($origin)!==$this->origin) {
                $event->setResponse(new Response('Origin rejected.',403));return;
            }
            if (strlen($r->getContent())>32768) { $event->setResponse(new Response('Request too large.',413)); }
        }
    }
    public function response(ResponseEvent $event):void {
        $h=$event->getResponse()->headers;
        $h->set('Cache-Control','no-store, private');
        $h->set('Pragma','no-cache');
        $h->set('Referrer-Policy','no-referrer');
        $h->set('X-Content-Type-Options','nosniff');
        $h->set('X-Frame-Options','DENY');
        $h->set('Content-Security-Policy',"default-src 'none'; style-src 'self'; img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");
        // HSTS is intentionally left to the validated deployment gateway; no includeSubDomains on bootstrap IPs.
    }
}
