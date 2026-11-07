<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
final class Configuration {
    public const PROFILES=['nginx_apache_fpm','nginx_fpm','apache_fpm','caddy_fpm','caddy_frankenphp'];
    public const MODULES=['dns','mail','database','sftp','backup'];
    public static function validate(array $data): array {
        $keys=['schema_version','admin_port','user_port','admin_host','user_host','webstack','modules'];
        if (array_diff(array_keys($data), $keys) || array_diff($keys, array_keys($data))) { throw new \InvalidArgumentException('Invalid configuration fields.'); }
        if ($data['schema_version']!==1) { throw new \InvalidArgumentException('Invalid schema.'); }
        foreach (['admin_port','user_port'] as $k) {
            if (!is_int($data[$k]) || $data[$k]<1024 || $data[$k]>65535) { throw new \InvalidArgumentException('Ports must be integers in 1024..65535.'); }
        }
        if ($data['admin_port']===$data['user_port']) { throw new \InvalidArgumentException('Ports must differ.'); }
        foreach (['admin_host','user_host'] as $k) {
            if (!is_string($data[$k]) || !self::hostname($data[$k])) { throw new \InvalidArgumentException('Use lowercase ASCII hostnames without scheme or port.'); }
        }
        if ($data['user_host']!=='' && ($data['admin_host']==='' || $data['admin_host']===$data['user_host'])) { throw new \InvalidArgumentException('User and admin portals require distinct hostnames.'); }
        if (!in_array($data['webstack'], self::PROFILES, true)) { throw new \InvalidArgumentException('Unknown webstack.'); }
        if (!is_array($data['modules']) || !array_is_list($data['modules'])) { throw new \InvalidArgumentException('Invalid modules.'); }
        $seen=[];
        foreach ($data['modules'] as $module) {
            if (!is_string($module) || !in_array($module, self::MODULES, true) || isset($seen[$module])) { throw new \InvalidArgumentException('Unknown or duplicated module.'); }
            $seen[$module]=true;
        }
        return $data;
    }
    private static function hostname(string $name): bool {
        if ($name==='') { return true; }
        if (strlen($name)>253 || !str_contains($name,'.') || $name!==strtolower($name)) { return false; }
        foreach (explode('.', $name) as $part) { if (!preg_match('/\A[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\z/D', $part)) { return false; } }
        return true;
    }
}
