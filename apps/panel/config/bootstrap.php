<?php
declare(strict_types=1);
use Symfony\Component\Dotenv\Dotenv;

// This file is not a credential source. On a managed host APP_* and FORGE_*
// values can be injected by a protected systemd EnvironmentFile or by CI.
// No .env file is created or sourced automatically from .env.example.
$dotenv = new Dotenv();
$localEnv = dirname(__DIR__).'/.env';
if (is_file($localEnv)) {
    $dotenv->bootEnv($localEnv);
}
// Retain the original protected-file precedence for verified installations.
if (is_file('/etc/forgepanel/panel.env')) {
    $dotenv->overload('/etc/forgepanel/panel.env');
}
$secret = $_SERVER['APP_SECRET'] ?? $_ENV['APP_SECRET'] ?? getenv('APP_SECRET');
if (!is_string($secret) || strlen($secret) < 32) {
    throw new RuntimeException('Provision a random APP_SECRET before starting the panel.');
}