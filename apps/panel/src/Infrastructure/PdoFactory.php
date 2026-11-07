<?php
declare(strict_types=1);
namespace ForgePanel\Infrastructure;
final class PdoFactory {
    public static function create(string $dsn,string $user,string $password): \PDO {
        if (!str_starts_with($dsn,'pgsql:')) { throw new \RuntimeException('PostgreSQL is required.'); }
        return new \PDO($dsn,$user,$password,[\PDO::ATTR_ERRMODE=>\PDO::ERRMODE_EXCEPTION,\PDO::ATTR_EMULATE_PREPARES=>false]);
    }
}
