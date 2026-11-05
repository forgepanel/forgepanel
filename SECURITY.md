# Security policy

[Detailed policy](DOCUMENTATION/en/10-security/README.md) · [Politique en français](DOCUMENTATION/fr/10-security/README.md)

## Current support

No production release or supported deployment exists in this repository. Foundation v0.6/v0.7 are supplied development archives, not security-certified products. No independent security audit is claimed.

## Reporting a vulnerability

Do not disclose secrets, customer data or actionable exploit details in a public issue. Use GitHub private vulnerability reporting **only if the repository actually exposes that feature**. The owner selected **both GitHub private vulnerability reporting and a dedicated security email**, with triage, tracking and notifications (Q118 C). Their actual availability, mailbox/recipients and private reporting configuration **have not yet been verified**. Do not invent an email address or claim either channel is operational until configured and tested. See [the Q111–Q120 policy](DOCUMENTATION/en/00-project-control/decisions-q111-q120.md). When no private channel is available, ask the owner for one without including sensitive details. Establishing that channel is a tracked prerequisite for public distribution.

For non-sensitive reports, give the affected commit/component, expected behavior, sanitized reproduction and impact. Avoid real credentials and production endpoints. Coordinate remediation privately before publishing a security advisory. The Q130 policy also calls for an **appointed security lead and deputy**, permissioned triage, escalation and coordinated notices. **Neither person nor the two private reporting channels is verified as operational today.** For Q127 private beta, review rights/conditions for every external recipient and verify the security routes **before** granting tester access. See [Q121–Q130](DOCUMENTATION/en/00-project-control/decisions-q121-q130.md).

No response SLA is promised before a maintained release and reporting process exist.

Keep deployment secrets, private signing keys, billing/license credentials and customer information outside the public project. Access to this private repository is not authorization to publish it or deploy its contents.
