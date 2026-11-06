<!-- forgepanel-doc id=FP-11 revision=5 status=documented -->
# Design system and internationalization

[Français](../../fr/11-design-system/README.md) · [Index](../README.md)

## Established identity

Product: **ForgePanel — The Modern Linux Server Control Panel**. Signature: **Modern • Secure • Modular • Scalable**. No approved logo, color palette, font license or complete visual component library is evidenced. Earlier illustrative mockups are not shipped interfaces.

The frontend baseline is Twig with Symfony UX/Stimulus and selectively Turbo/Live Components. SRC-03 contains Twig setup templates and `public/assets/setup.css`; it does not contain a deployed Tailwind/UX design system. Keep that distinction when planning asset compilation and dependencies.

## FORGE and PANEL interface isolation

The target keeps distinct portal surfaces with separate paths, ports, sessions and assets: **FORGE `/forge`: 8447** and **PANEL `/panel`: 8446**, using the detected host IP and existing verified FQDN if any (no customizable domain or automatic 443 vhost). Each portal has independent header, sidebar and theme variables; reusable components remain contract- and permission-bound. CSS/JS bundles are isolated to avoid collisions and unauthorized loading. A mockup does not implement routing or RBAC. [Access contract](../07-interfaces-roles/portal-access-routing.md) · [Planned tests](../13-tests-quality/portal-access-gates.md).

## Required interaction states

Every actionable component must distinguish idle, loading, success, empty, validation error, permission denial, interrupted and partial-failure states. A queued job is not completed work. Show changes and affected resources before sensitive actions; avoid irreversible one-click repair. The wizard preserves progress and shows a reviewed draft separately from an applied configuration. Technical errors must have a correlation reference without exposing secrets.

Use explicit labels, keyboard navigation, visible focus, understandable field errors, non-color status cues and responsive layouts. Test contrast, zoom and screen-reader navigation before making accessibility claims. Do not rely on browser screenshots alone for functional or security validation.

## Internationalization strategy

Target stable English translation keys in Symfony translation catalogs with French and English messages, locale-aware dates/numbers and a documented fallback. Protocol values, operation IDs and log codes stay language-neutral. Do not translate permission names or schema keys. SRC-03's literal template text is a prototype, not a completed translation infrastructure.

Each new screen needs both locales, long-text and small-screen cases, permission-denied states and secret-redaction tests. Product language choices and a production design token set remain to be specified; this chapter introduces no new frontend framework.

Q70 D adds a [visual theme/layout/widget/navigation editor](visual-editor.md) using Symfony Twig/UX. Q55 A preserves **one brand per organization**. Components must be schema-validated, accessible and permissioned; arbitrary JavaScript/PHP is not accepted. This is not implemented.

Q80 confirms **official and approved-partner widgets** plus **declarative custom widgets** using allowlisted data sources, validated props and scoped permissions. Widgets are not unrestricted PHP/JS programs; keep Symfony/Twig/UX and one brand per organization. See [visual editor](visual-editor.md) and [Q71–Q80](../00-project-control/decisions-q71-q80.md).

[Interfaces](../07-interfaces-roles/README.md) · [Quality](../13-tests-quality/README.md)
