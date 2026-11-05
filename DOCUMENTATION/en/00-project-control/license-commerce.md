<!-- forgepanel-doc id=FP-00-LICENSE revision=1 status=specified -->
# AGPL-3.0 / commercial dual licensing and paid-offer protection

[Français](../../fr/00-project-control/license-commerce.md) · [Decisions](decisions.md) · [Product policy](product-policy.md)

## Confirmed owner choices — 2026-11-05

- **Q48 A**: **GNU AGPL-3.0 + commercial license** for the ForgePanel Core. Whether to use `AGPL-3.0-only` or `AGPL-3.0-or-later`, exact commercial terms and per-file notices still need approval before an operative license is published; no `LICENSE` has been installed yet.
- **Q49 A**: external contributions require a **Contributor License Agreement (CLA)** granting the publisher sufficient rights to offer both licenses, with author rights governed by the CLA. Legal entity, signature workflow, minor/company authority, consent and DCO interaction remain to be defined and reviewed.
- **Q50 B**: complete free Core, optional **specialist plugins**, cloud/managed services, partner offerings and paid support. No subscription is needed for the free Core, bootstrap, repair or essential hosting.
- **Owner clarification**: “protect our product unless [the customer] pays for modules and subscription”. This is interpreted **only for separately licensed commercial products**: premium downloads, subscriptions and publisher services require valid contractual entitlements checked through Hub. It **cannot** remove rights granted to lawful recipients of the AGPL Core.

## AGPL freedoms versus monetization

AGPL recipients may use, study, modify and redistribute the work on its terms. The publisher may **sell** alternative licenses, initial access to some delivery channels, support and services, but cannot add a mandatory payment or telemetry condition to AGPL rights for copies lawfully obtained. Modified versions used through a network require offering corresponding source to affected remote users under AGPL terms.

The copyright owner may dual-license its own code, but must track rights in third-party contributions, dependencies and derivative works. **Separate repositories/processes do not automatically make a proprietary plugin independent of AGPL obligations.** Review actual coupling and distribution before shipping closed-source premium modules.

## Commercially protectable assets

| Asset | Intended protection | Constraint |
|---|---|---|
| ForgePanel Core | Copyright, AGPL compliance, alternative commercial grant, provenance/quality | No fee to exercise AGPL rights |
| Name and logo | Trademark/brand guidelines and official identity; registration to study | Trademark rights differ from code license |
| Independent premium packages | Authorized delivery, purchase/subscription grants, signatures and update rights | Verify license and actual legal separation before distribution |
| Hub/cloud/support services | Authentication, verified payments, subscriptions, API quotas | Commercial outage cannot disable Core sites |
| Signing pipeline | Private publisher keys, signed releases, partner approval and response to compromised artifacts | Signatures do not prove safety |
| Customer installations | **Premium-only** entitlement checks; 60-day eligible offline grace | No mandatory Core telemetry or destructive remote controls |

## Contribution and provenance prerequisites

The CLA must identify publisher/legal entity, copyright/patent grants, explicit dual-licensing authority and authorized contributors. Retain proof of acceptance before licensing a contribution commercially. Audit third-party dependency grants; code not eligible for alternative licensing needs exclusion or additional rights. A CLA does not magically relicense unrelated third-party code.

## States and pending choices

**CONFIRMED**: AGPL-3.0 plus commercial, CLA, full free Core, optional premium/services/support. **OPEN**: only/or-later AGPL, commercial grant text, precise closed-module coupling/license, trademark entity and subscription contract. **NOT IMPLEMENTED**: operative Core licenses, entitlement service and premium ecosystem.

Background: [GNU FAQ](https://www.gnu.org/licenses/gpl-faq.en.html), [GNU AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html) and [CLA considerations](https://interoperable-europe.ec.europa.eu/collection/eupl/licences-complementary-agreements). Product specification, not legal advice.
