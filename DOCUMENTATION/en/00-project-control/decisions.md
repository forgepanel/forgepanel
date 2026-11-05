<!-- forgepanel-doc id=FP-00-DECISIONS revision=1 status=documented -->
# Decision register

[Français](../../fr/00-project-control/decisions.md) · [Project control](README.md)

Source IDs refer to the [baseline](../19-audits-risks/baseline.md). A decision adopted as a design baseline is not evidence of implementation.

| ID | Decision and authority | State / consequence |
|---|---|---|
| ADR-001 | ForgePanel is the new product; WCP360 is historical context (SRC-02) | Confirmed identity; no automatic WCP360 code/licensing/commercial inheritance |
| ADR-002 | Symfony/PHP + Twig/UX; Go for system operations; PostgreSQL (SRC-02, SRC-03 manifest) | Design baseline; archive has Twig but not installed UX/Tailwind/Messenger dependencies |
| ADR-003 | Multi-OS from the start (explicit owner request, SRC-02) | Required: Debian 12/13; Ubuntu and AlmaLinux; archive planning matrix selects 24.04/26.04 and 9/10; no certification |
| ADR-004 | Composable web engines, five profile IDs (SRC-02/03) | Specified; profile selection exists, service provisioning does not |
| ADR-005 | One-command installation followed by web setup and CLI recovery (owner, SRC-02) | Required outcome; not delivered by `install plan` |
| ADR-006 | Bootstrap token instead of Linux password in browser (SRC-02/03) | Retained security baseline; application super-admin is not Linux root |
| ADR-007 | PostgreSQL owns web bootstrap transaction (SRC-03) | Archive implementation supersedes v0.6 file-token integration; SQL integration unverified |
| ADR-008 | Direct ports 8447/8446 and distinct portal hosts (SRC-02/03) | Prototype defaults; 446/447 suggestion not retained; USER remains closed; port changes do not isolate cookies |
| ADR-009 | Bilingual documentation, one changelog, four permanent branches (explicit owner, SRC-01) | Governs this change; no release/deployment is authorized merely by branch creation |
| ADR-010 | Application runtime policy | Open: archive accepts PHP >=8.2; earlier PHP 8.4 preference is not a certified six-OS package policy |
| ADR-011 | License and contribution terms | Open owner decision; no AGPL, GPL, proprietary or dual-license assumption |
| ADR-012 | Documentation tooling uses Python standard library only | New bounded tooling choice; does not make Python a product runtime dependency |
| ADR-013 | Administrator MFA optional (explicit owner decision, 2026-11-05) | Initial account without mandatory TOTP; enroll now or later, sensitive step-up; v0.7 source still blocks setup until corrected on import. |
| ADR-014 | ForgePanel-Hub as private detached publisher extension in `yyogas/forgepanel-hub` | Same standard Core with or without Hub; generic ABI absent; never inject private PHP or grant root. |

## Replaced or unresolved proposals

Vue as the main frontend and Debian-only delivery were replaced by the later Symfony-native frontend and multi-OS requirement. Python and Redis remain optional, not mandatory core services. TOTP enrollment exists in the archive; WebAuthn and permanent authentication remain future work. Prior claims of a working agent, full installer or official public release are not supported by the observed repository.

New decisions must record context, alternatives, rationale, affected contracts, validation and any replaced decision. Changing a requirement requires explicit reconciliation rather than quietly editing history.
