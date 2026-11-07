<?php
declare(strict_types=1);
namespace ForgePanel\Command;
final class LocalConsoleGuard {
    public static function enforce(bool $secret):void {
        if (PHP_SAPI!=='cli' || getenv('FORGEPANEL_LOCAL_BOOTSTRAP')!=='1' || !function_exists('posix_geteuid')) {
            throw new \RuntimeException('Use the installed, local sudo forgepanel setup CLI.');
        }
        $uid=posix_geteuid();$account=posix_getpwuid($uid);
        if ($uid===0 || !is_array($account) || $account['name']!=='forgepanel') {
            throw new \RuntimeException('The Go CLI must drop privileges to the dedicated forgepanel account.');
        }
        if ($secret && (!function_exists('stream_isatty') || !stream_isatty(STDOUT))) {
            throw new \RuntimeException('Secrets may only be printed to a controlling terminal.');
        }
    }
}
