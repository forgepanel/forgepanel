-- Development schema. Apply with the local migration command, not per HTTP request.
-- Use a dedicated database. Runtime roles must not have DDL privileges in production.
CREATE TABLE IF NOT EXISTS fp_setup (
    singleton smallint PRIMARY KEY CHECK (singleton = 1),
    payload jsonb NOT NULL
);
INSERT INTO fp_setup(singleton,payload) VALUES (1,
'{"version":1,"phase":"NEW","token_hash":null,"token_expiry":0,"attempts":0,"grant_hash":null,"grant_expiry":0,"admin_id":null,"mfa_attempts":0,"config_revision":0,"config":null,"resume_hash":null,"resume_expiry":0,"resume_attempts":0}'::jsonb
) ON CONFLICT (singleton) DO NOTHING;
CREATE TABLE IF NOT EXISTS fp_admins (
    id uuid PRIMARY KEY,
    email varchar(254) NOT NULL UNIQUE,
    password_hash text NOT NULL,
    role text NOT NULL DEFAULT 'ROLE_SUPER_ADMIN' CHECK (role = 'ROLE_SUPER_ADMIN'),
    initial_admin boolean NOT NULL DEFAULT false,
    mfa_secret text NOT NULL,
    mfa_enabled boolean NOT NULL DEFAULT false,
    last_totp_counter bigint,
    recovery_hashes jsonb NOT NULL DEFAULT '[]',
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS fp_single_initial_admin ON fp_admins(initial_admin) WHERE initial_admin;
CREATE TABLE IF NOT EXISTS fp_setup_audit (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event varchar(80) NOT NULL,
    metadata jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
