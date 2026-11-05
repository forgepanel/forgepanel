<!-- forgepanel-doc id=FP-11 revision=1 status=documented -->
# Design system and internationalization

[Français](../../fr/11-design-system/README.md) · [Index](../README.md)

## Established identity

Product: **ForgePanel — The Modern Linux Server Control Panel**. Signature: **Modern • Secure • Modular • Scalable**. No approved logo, color palette, font license or complete visual component library is evidenced. Earlier illustrative mockups are not shipped interfaces.

The frontend baseline is Twig with Symfony UX/Stimulus and selectively Turbo/Live Components. SRC-03 contains Twig setup templates and `public/assets/setup.css`; it does not contain a deployed Tailwind/UX design system. Keep that distinction when planning asset compilation and dependencies.

## Required interaction states

Every actionable component must distinguish idle, loading, success, empty, validation error, permission denial, interrupted and partial-failure states. A queued job is not completed work. Show changes and affected resources before sensitive actions; avoid irreversible one-click repair. The wizard preserves progress and shows a reviewed draft separately from an applied configuration. Technical errors must have a correlation reference without exposing secrets.

Use explicit labels, keyboard navigation, visible focus, understandable field errors, non-color status cues and responsive layouts. Test contrast, zoom and screen-reader navigation before making accessibility claims. Do not rely on browser screenshots alone for functional or security validation.

## Internationalization strategy

Target stable English translation keys in Symfony translation catalogs with French and English messages, locale-aware dates/numbers and a documented fallback. Protocol values, operation IDs and log codes stay language-neutral. Do not translate permission names or schema keys. SRC-03's literal template text is a prototype, not a completed translation infrastructure.

Each new screen needs both locales, long-text and small-screen cases, permission-denied states and secret-redaction tests. Product language choices and a production design token set remain to be specified; this chapter introduces no new frontend framework.

[Interfaces](../07-interfaces-roles/README.md) · [Quality](../13-tests-quality/README.md)
