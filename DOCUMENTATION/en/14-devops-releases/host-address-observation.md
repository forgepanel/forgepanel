<!-- forgepanel-doc id=FP-14-HOST-OBSERVE revision=2 status=specified -->
# Host IP and optional OS DNS observation — independent R3 preparation

[Français](../../fr/14-devops-releases/host-address-observation.md) · [DevOps](README.md) · [Tools](../../../tools/host-address-observation/README.md)

## State and boundaries

The standalone Go module under [tools/host-address-observation](../../../tools/host-address-observation/README.md) has two distinct CLI tools. **`forgepanel-host-observe`** reads the local OS interface/IP inventory and its FQDN candidate without networking. **`forgepanel-dns-observe --observe`** makes a single, optional, bounded OS-resolver A/AAAA lookup for that discovered candidate only. The DNS command will make a network query if the system resolver requires one, so it is never invoked implicitly. No arbitrary hostname arguments, root/shell execution, system mutation or external public-IP provider are included. Both commands are preparatory prototypes, not Core integration, HTTPS or OS certification.

The owner's fixed portal paths/ports remain **FORGE `/forge:8447`** and **PANEL `/panel:8446`**. There is no customizable domain input or implicit 443 virtual host. The same verified FQDN might eventually serve both ports, but that is **not** established by this prototype.

## Interpretation and safety

- The OS interface listing is partial-capable, filtered, sorted and deduplicated. Non-private/unicast **does not prove** that an address is public, or reachable through NAT/firewall.
- A syntactically valid FQDN from the OS is only `CANDIDATE_UNVERIFIED`. No FQDN produces `NO_FQDN` and **no** DNS query.
- The optional resolver can return `MATCHED_LOCAL_OS_RESOLVER_ONLY` when all accepted responses match assigned local interface IPs; a mismatch returns `NAT_OR_REMOTE_ROUTING_UNVERIFIED`. These are **unverified** in all cases. Local resolver sources may include `/etc/hosts`, search configuration and split-horizon DNS.
- Resolver queries are time- and answer-limited, rejecting loopback/unusable answers, de-duplicating IPv4/IPv6 and redacting raw resolver errors to fixed warning codes.
- The DNS report always has `dns_authority_verified=false`, `public_reachability=NOT_EXECUTED`, `tls_verification=NOT_EXECUTED`, `listener_verification=NOT_EXECUTED` and empty `verified_access_urls`.
- These CLI tools do **not** verify a certificate with IP-SAN or FQDN SAN, prove A/AAAA from an independent external network, test HTTPS port 8447/8446 or generate a clickable working URL.

## Tests and prerequisites

The [dedicated workflow](../../../.github/workflows/host-address-observation.yml) runs offline Go tests, the race detector, `go vet`, an OS inventory no-URL invariant and a test that DNS CLI refuses a missing opt-in flag. Offline tests inject fake resolver responses; they do not query live DNS. The first real Core endpoint still depends on source import #2, Symfony/PostgreSQL #3, the installer and security review; [issue #51](https://github.com/yyogas/forgepanel/issues/51) remains open for integrated DNS/TLS/proxy/cookie/VM checks. This stand-alone source must not be published as installed Core.

**Status: stand-alone source candidate only; no verified domain, HTTPS endpoint, Core deployment or external reachability evidence.**
