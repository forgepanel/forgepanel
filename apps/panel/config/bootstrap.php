<?php
declare(strict_types=1);
use Symfony\Component\Dotenv\Dotenv;
(new Dotenv())->bootEnv(dirname(__DIR__).'/.env');
// Installed deployments use a dedicated root-managed, service-readable file.
if (is_file('/etc/forgepanel/panel.env')) {
    (new Dotenv())->overload('/etc/forgepanel/panel.env');
}
if (strlen((string)($_SERVER['APP_SECRET']??$_ENV['APP_SECRET']??''))<32) {
    throw new RuntimeException('Provision a random APP_SECRET before starting the panel.');
}
