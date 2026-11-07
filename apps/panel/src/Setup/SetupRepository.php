<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
interface SetupRepository {
    /** The callback runs under an exclusive lock on the singleton bootstrap row.
     *  All state, account and audit writes commit together, or all roll back. */
    public function transaction(callable $operation): mixed;
}
