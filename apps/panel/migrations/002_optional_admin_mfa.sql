-- Follow 001_setup.sql. Initial MFA is explicitly optional.
-- Existing confirmed MFA remains enabled. Pending enrollment secrets are
-- cleared ONLY after an explicit skip choice by the account holder.
ALTER TABLE fp_admins ALTER COLUMN mfa_secret DROP NOT NULL;
