<!-- forgepanel-doc id=FP-17 revision=4 status=documented -->
# User and administrator guidance

[Français](../../fr/17-user-guides/README.md) · [Index](../README.md)

## What the owner can use now

Use this documentation to state priorities and review product outcomes. The technical agent handles code, testing and corrections. There is no published installation command, working hosting portal or production support procedure to run from this repository. Supplied archives are development inputs, not customer installers.

## Intended first-install journey

A future verified one-command installer checks the server, installs the panel independently of customer stacks and prints a verified HTTPS setup address. The owner obtains a one-use code from the privileged local terminal, creates a panel administrator independent of Linux root, may enable or skip MFA and chooses server services in a resumable wizard. The plan explains changes before application. A completed wizard must distinguish selected services from actually installed and healthy ones.

The current archive only prototypes enrollment and configuration export. Do not enter the server's Linux password into an unverified web form. Do not bypass a TLS identity warning just to complete bootstrap. Example hostnames are documentation values, not official service endpoints.

## Choosing a site's WebStack (Q79)

The target website workflow presents **a WebStack recommended for that individual site**, with reasons and compatible alternatives. The site administrator may select before creation and later request **a profile switch** using preview, security tests and recovery plans; changing one site must not modify all websites. [Specification](../02-architecture/site-webstack-advisor.md). These screens have not been implemented.

## Target website management (Q81–Q90)

Each authorized operator can inspect a WebStack recommended for the individual site (application/`.htaccess`/PHP/isolation/resources/listeners), choose a compatible profile and request a later switch with preview, maintenance notice, test route or progressive cutover **only when feasible**. Future screens cover PHP/extensions/FPM, ACME/wildcard certificates, Git Deploy/staging, databases/cache, files/SFTP/restricted SSH, mail/webmail, quotas and selective restore/clone. **None is currently operational.** [Specification](../00-project-control/decisions-q81-q90.md).

## Q91–Q100 future website settings

Authorized site operators will see maintained PHP versions and EOL alerts, qualify hardened FPM profiles, select manual/authenticated-webhook Git Deploy and configure private staging with retention, masking and independent secrets. TLS can use multiple ACME/DNS-01 issuers, account SQL/cache engines are allocated by quota, SSH keys expire/revoke, compatible Webmail is selectable, quota grace requires admin permission and cross-server migration is previewed. **No operational screens are shipped**; all actions require authorization and validation. [Q91–Q100 specification](../00-project-control/decisions-q91-q100.md).

## Customer and reseller journeys

Customer site/domain/file/database/mail/backup actions and reseller delegation are intended capabilities, not usable screens in this baseline. Their guides will be written with verified screenshots and permission/error paths after implementation. A customer must not gain admin authority by changing a port or URL.

## Help and recovery

Report non-sensitive symptoms, product revision and sanitized errors to the project owner/maintainer. Never post passwords, bootstrap codes, MFA secrets, customer files or signing keys. An access or product decision may require owner intervention; programming corrections do not. Existing prototype CLI limits are documented in [operations](../15-operations/README.md). The roadmap gives the next deliverables without asking the owner to edit code.
