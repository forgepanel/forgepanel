<!-- forgepanel-doc id=FP-12-OPTIONAL-ADMIN-MFA-071 revision=1 status=documented -->
# Foundation v0.7.1 — optional initial administrator MFA patch (stacked draft)

[Français](../../fr/12-development/foundation-v071-optional-mfa.md) · [Source import](foundation-v07-source-import.md) · [Pinned patch inventory](../../evidence/foundation-v071-optional-mfa-patch.json)

## Purpose and exact scope

The owner explicitly selected **optional administrator MFA**. The historical Foundation v0.7 prototype incorrectly required initial TOTP enrollment for server configuration. This **11-file candidate patch**, taken byte-for-byte from the separate recovered v0.7.1 optional-MFA archive (SHA-256 `83fe6e77713f68d69595e74864aa1c33f75d88b6ba4199e03d5ef30a7060402c`), introduces an explicit skip decision protected by the current setup grant, CSRF and a bounded rate limit. It clears the pending encrypted enrollment secret, denies repeat skip, records a redacted audit event, and then permits configuration. Confirmed MFA remains enabled. There is **one additive migration** following `001_setup.sql`: `ALTER TABLE fp_admins ALTER COLUMN mfa_secret DROP NOT NULL;`.

The code still cannot boot a verified real Symfony application, prove PostgreSQL concurrency or install ForgePanel. The 30 PHP domain tests (199 assertions) and Go native tests passed independently with no root access and no live database. A security review must inspect the transaction boundary, session/grant binding and migration upgrade/downgrade. Exact released version, package signature and runtime certifications are **not** established.

## Reproducible source checks

```sh
python3 scripts/check_foundation_import.py
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
bash scripts/check.sh
```

The source import manifest for v0.7 stays pinned, while the separate 11-entry patch manifest supplies each verified before/after digest. The checker rejects changed hashes, missing migration, false release certifications and original `.env` files. `install apply` remains blocked. The patch is stacked on top of the [base R1 source PR](foundation-v07-source-import.md) for focused review, not a merge authorization.

**Required before R2:** actual Symfony HTTPS/origin/CSRF/browser tests for both explicit skip and real enrollment, authenticated account recovery, PostgreSQL migration/rollback and concurrency tests. No Hub service is a prerequisite, and existing Q1–Q220 decisions are preserved.