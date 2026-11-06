# ForgePanel — Host address observation preflight

This is a standalone **read-only, unprivileged Go utility**, not the imported Foundation Core, not the Symfony application and not an installer, running agent or HTTPS gateway.

It inventories IPv4/IPv6 addresses of up, non-loopback OS interfaces and extracts a syntactically valid system FQDN **candidate** if one exists. It preserves the owner-confirmed FORGE /forge port 8447 and PANEL /panel port 8446 contract. It does not accept a custom domain, generate subdomains or configure a virtual host on port 443.

**It never verifies DNS, TLS, NAT/public reachability or active listeners.** Its verified_access_urls is always empty; all verification fields are NOT_EXECUTED. A machine address, even non-private, is not proof of a public IP. An OS hostname may be local or controlled by /etc/hosts. Report data may be sensitive; keep locally or redact before sharing.

To run from this directory with Go 1.23 or compatible, without network downloads:

    GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...
    GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test -race ./...
    GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go vet ./...
    GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-host-observe

The command is read-only and takes no arguments. No DNS query, HTTP call, subprocess, socket listener, OS configuration mutation, filesystem write, root privilege or external IP-detection service is required.

The original Foundation v0.7 archive is still missing from the tracked Core. This helper is an **independent preparatory prototype**, not a replacement for it. A future reviewed Core integration must first pass source import R1, Symfony/PostgreSQL R2 and real TLS/network certification R3/R4.

[French specification](../../DOCUMENTATION/fr/14-devops-releases/host-address-observation.md) · [English specification](../../DOCUMENTATION/en/14-devops-releases/host-address-observation.md) · [Portal contracts PR #50](https://github.com/yyogas/forgepanel/pull/50) · [Runtime issue #51](https://github.com/yyogas/forgepanel/issues/51).
