# ForgePanel — Host address and optional DNS evidence preflight

This is a standalone **unprivileged Go preflight prototype**, not Foundation Core, Symfony, an installer, a daemon, a proxy, or a certified hosting panel.

## Two separate modes

**1. OS inventory only — no network query**

```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-host-observe
```

Reports assigned IPv4/IPv6 from active non-loopback interfaces and an optional syntactically valid local hostname/FQDN **candidate**. Shows immutable FORGE `/forge:8447` and PANEL `/panel:8446` metadata. Does **not** accept a custom portal domain, create subdomains, configure HTTPS port 443, or generate working URLs.

**2. Optional OS-resolver evidence — may trigger DNS traffic**

```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-dns-observe --observe
```

This separate command is **only called with explicit `--observe`**; without the flag it fails without a lookup. It performs at most one bounded OS-resolver lookup (4-second context timeout, 32-answer limit) for the already discovered **machine hostname candidate**, never a freely supplied hostname or a public IP lookup service. `/etc/hosts`, local resolver rules, cache and split DNS can affect its results. Comparing A/AAAA answers with OS interface addresses provides local consistency evidence, **not proof of publicly authoritative DNS, a valid certificate, network reachability or a working portal**.

Possible statuses: `NO_FQDN`, `MATCHED_LOCAL_OS_RESOLVER_ONLY`, `NAT_OR_REMOTE_ROUTING_UNVERIFIED`, `NO_ADDRESS_ANSWERS_UNVERIFIED`, `REJECTED_RESOLVER_ANSWERS_UNVERIFIED`, `TOO_MANY_ANSWERS_UNVERIFIED`, `RESOLVER_ERROR_UNVERIFIED`. Both commands always leave `verified_access_urls` empty; no certificate authority, listener or public reachability is checked. Hostnames, IPs and diagnostics can be sensitive: do not upload reports without authorization and redaction.

## Offline tests (do not perform DNS lookups)

```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go vet ./...
```

The original Foundation v0.7 archive still has not been imported. This helper is an **independent preparatory prototype**; production DNS verification must use separately approved independent DNS observations, NAT/routing checks, verified HTTPS certificates and actual VM/HTTP tests after R1/R2 integration.

[FR specification](../../DOCUMENTATION/fr/14-devops-releases/host-address-observation.md) · [EN specification](../../DOCUMENTATION/en/14-devops-releases/host-address-observation.md) · [Portal contract PR #50](https://github.com/yyogas/forgepanel/pull/50) · [Core integration issue #51](https://github.com/yyogas/forgepanel/issues/51).
