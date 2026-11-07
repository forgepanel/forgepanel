<?php
declare(strict_types=1);
use ForgePanel\Kernel;
use Symfony\Component\HttpFoundation\Request;
require dirname(__DIR__).'/vendor/autoload.php';
require dirname(__DIR__).'/config/bootstrap.php';
$kernel=new Kernel('prod',false);
$request=Request::createFromGlobals();
$response=$kernel->handle($request);
$response->send();
$kernel->terminate($request,$response);
