<?php
declare(strict_types=1);
namespace ForgePanel\Controller;
use ForgePanel\Setup\{SetupService,Configuration};
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\HttpFoundation\{Request,Response,JsonResponse};
use Symfony\Component\RateLimiter\RateLimiterFactory;
use Symfony\Component\Routing\Attribute\Route;
final class SetupController extends AbstractController {
    public function __construct(private SetupService $setup,
        #[Autowire(service:'limiter.setup_ip')] private RateLimiterFactory $limiter) {}
    private function grant(Request $r):string { return (string)$r->getSession()->get('setup_grant',''); }
    private function csrf(Request $r,string $id):void {
        if (!$this->isCsrfTokenValid($id,(string)$r->request->get('_token',''))) { throw $this->createAccessDeniedException('Invalid CSRF token.'); }
    }
    private function limit(Request $r):void {
        if (!$this->limiter->create($r->getClientIp()??'unknown')->consume(1)->isAccepted()) {
            throw new \Symfony\Component\HttpKernel\Exception\TooManyRequestsHttpException(300,'Try again later.');
        }
    }
    private function attach(Request $r,string $grant):void {
        $session=$r->getSession();$session->clear();$session->migrate(true);$session->set('setup_grant',$grant);
    }
    private function problem(\Throwable $e):string {
        if ($e instanceof \DomainException || $e instanceof \InvalidArgumentException) { return $e->getMessage(); }
        error_log('ForgePanel setup infrastructure failure: '.$e::class);
        return 'Setup is unavailable. Use the local CLI; no system installation was performed.';
    }
    #[Route('/setup',name:'setup_register',methods:['GET','POST'])]
    public function register(Request $r):Response {
        $error=null;
        if ($r->isMethod('POST')) {
            $this->csrf($r,'setup-register');$this->limit($r);
            try {
                $res=$this->setup->register((string)$r->request->get('bootstrap_token',''),(string)$r->request->get('email',''),(string)$r->request->get('password',''));
                if ($res['ok']) { $this->attach($r,$res['grant']);return $this->redirectToRoute('setup_mfa',[],303); }
                $error='Authorization invalid, expired or exhausted. Regenerate locally if no administrator exists.';
            } catch (\Throwable $e) { $error=$this->problem($e); }
        }
        return $this->render('setup/register.html.twig',['error'=>$error],new Response('', $error?422:200));
    }
    #[Route('/setup/resume',name:'setup_resume',methods:['GET','POST'])]
    public function resume(Request $r):Response {
        $error=null;
        if ($r->isMethod('POST')) {
            $this->csrf($r,'setup-resume');$this->limit($r);
            try {
                $res=$this->setup->redeemResume((string)$r->request->get('resume_token',''));
                if (!$res['ok']) { throw new \DomainException('Invalid resume authorization.'); }
                $progress=$res;$this->attach($r,$res['grant']);
                return $this->redirectToRoute($progress['phase']==='MFA_PENDING'?'setup_mfa':'setup_configuration',[],303);
            } catch (\Throwable $e) { $error='Invalid or expired local recovery authorization.'; }
        }
        return $this->render('setup/resume.html.twig',['error'=>$error],new Response('',$error?422:200));
    }
    #[Route('/setup/mfa',name:'setup_mfa',methods:['GET','POST'])]
    public function mfa(Request $r):Response {
        $error=null;
        try {
            $enrollment=$this->setup->enrollment($this->grant($r));
            if ($r->isMethod('POST')) {
                $this->csrf($r,'setup-mfa');$this->limit($r);
                $res=$this->setup->confirmMfa($this->grant($r),(string)$r->request->get('code',''));
                if ($res['ok']) { $r->getSession()->set('recovery_codes',$res['recovery_codes']);return $this->redirectToRoute('setup_recovery',[],303); }
                $error='Invalid MFA code or attempt limit reached. Local setup resume can reset enrollment attempts.';
            }
        } catch (\DomainException $e) { return $this->redirectToRoute('setup_resume'); }
        return $this->render('setup/mfa.html.twig',['error'=>$error,'enrollment'=>$enrollment],new Response('',$error?422:200));
    }
    #[Route('/setup/recovery',name:'setup_recovery',methods:['GET','POST'])]
    public function recovery(Request $r):Response {
        try { $progress=$this->setup->progress($this->grant($r)); } catch (\DomainException) { return $this->redirectToRoute('setup_resume'); }
        if (!in_array($progress['phase'],['CONFIGURING','REVIEWED'],true)) { return $this->redirectToRoute('setup_mfa'); }
        if ($r->isMethod('POST')) { $this->csrf($r,'setup-recovery');$r->getSession()->remove('recovery_codes');return $this->redirectToRoute('setup_configuration',[],303); }
        $codes=$r->getSession()->get('recovery_codes',[]);
        if (!$codes) { return $this->redirectToRoute('setup_configuration'); }
        return $this->render('setup/recovery.html.twig',['codes'=>$codes]);
    }
    #[Route('/setup/configuration',name:'setup_configuration',methods:['GET','POST'])]
    public function configuration(Request $r):Response {
        try { $p=$this->setup->progress($this->grant($r)); } catch (\DomainException) { return $this->redirectToRoute('setup_resume'); }
        if (!in_array($p['phase'],['CONFIGURING','REVIEWED'],true)) { return $this->redirectToRoute('setup_mfa'); }
        $cfg=$p['config']??['admin_port'=>8447,'user_port'=>8446,'admin_host'=>'','user_host'=>'','webstack'=>'nginx_apache_fpm','modules'=>[]];$error=null;
        if ($r->isMethod('POST')) {
            $this->csrf($r,'setup-configuration');
            try {
                $cfg=['schema_version'=>1,'admin_port'=>filter_var($r->request->get('admin_port'),FILTER_VALIDATE_INT),
                    'user_port'=>filter_var($r->request->get('user_port'),FILTER_VALIDATE_INT),
                    'admin_host'=>(string)$r->request->get('admin_host',''),'user_host'=>(string)$r->request->get('user_host',''),
                    'webstack'=>(string)$r->request->get('webstack',''),'modules'=>$r->request->all('modules')];
                $revision=filter_var($r->request->get('revision'),FILTER_VALIDATE_INT);
                if ($revision===false) { throw new \InvalidArgumentException('Invalid form revision.'); }
                $this->setup->saveConfiguration($this->grant($r),$cfg,$revision);
                return $this->redirectToRoute('setup_review',[],303);
            } catch (\DomainException|\InvalidArgumentException $e) { $error=$e->getMessage(); }
        }
        return $this->render('setup/configuration.html.twig',['config'=>$cfg,'revision'=>$p['revision'],'profiles'=>Configuration::PROFILES,'modules'=>Configuration::MODULES,'error'=>$error],new Response('',$error?422:200));
    }
    #[Route('/setup/review',name:'setup_review',methods:['GET'])]
    public function review(Request $r):Response {
        try { $p=$this->setup->progress($this->grant($r)); } catch (\DomainException) { return $this->redirectToRoute('setup_resume'); }
        if ($p['phase']!=='REVIEWED') { return $this->redirectToRoute('setup_configuration'); }
        return $this->render('setup/review.html.twig',['config_json'=>json_encode($p['config'],JSON_PRETTY_PRINT|JSON_THROW_ON_ERROR),'revision'=>$p['revision']]);
    }
    #[Route('/setup/configuration.json',name:'setup_export',methods:['GET'])]
    public function export(Request $r):Response {
        try { $p=$this->setup->progress($this->grant($r)); } catch (\DomainException) { throw $this->createAccessDeniedException(); }
        if ($p['phase']!=='REVIEWED') { throw $this->createAccessDeniedException(); }
        return new JsonResponse($p['config'],200,['Content-Disposition'=>'attachment; filename="forgepanel-install.json"']);
    }
}
