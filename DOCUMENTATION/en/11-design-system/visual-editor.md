<!-- forgepanel-doc id=FP-11-VISUAL revision=2 status=specified -->
# Visual panel editor, widgets and navigation (Q70 D)

[Français](../../fr/11-design-system/visual-editor.md) · [Design system](README.md) · [Decisions](../00-project-control/infrastructure-decisions.md)

## Product decision and boundaries

The target UI stays **entirely Symfony-based**: Twig, Symfony UX Live Components, Stimulus, Turbo and Tailwind (light frontend tooling). The owner selected a **visual layout editor**, configurable widgets, customizable navigation, previews and revision history. Q55 A preserves **one brand per organization**; several layouts/scoped experiences can exist within that brand, not multiple separate brands.

## Q80 — official, partner and declarative widgets

The target catalog supports **official and approved-partner widgets** plus **custom declarative widgets**: composition of permitted existing data, bounded filters/aggregations, charts and layouts, without arbitrary script evaluation. Manifests specify owner, fields/resources, RBAC, schema version, query budgets and unavailable-data behavior. Displaying a source never grants new read privileges. One brand per organization (Q55) remains in force. [Decision Q80](../00-project-control/decisions-q71-q80.md).

## Customization model

Versioned `ThemeTokens`, `BrandAssets`, `Layout`, `DashboardWidget`, `NavigationItem`, `MenuSection`, `Localization`. Each declares stable ID, render contract/version, schema-validated props, permissions, role/scope, order and compatibility. Routes must be registered by Core or approved plugins. Hiding a menu item **does not grant or remove** server-side authorization.

Target audiences: Admin, User, reseller, collaborator; Standard/Advanced/Expert modes affect ergonomics, never RBAC. Organization settings include logo, favicon, palette, approved fonts, domain, email identity, widgets and navigation within parent policy, without exposing secrets or other tenants' data.

## Editor and publication

`DRAFT → PREVIEW (desktop/mobile) → VALIDATE (contrast, access, schema) → PUBLISH (version and audit) → REVERT`. Allow drag/drop, ordering, grid sizes, visibility and settings of **approved** widgets. The editor is not an untrusted PHP/JS/CSS interpreter; HTML and URLs are escaped/filtered. Unapproved plugin widgets receive no elevated privileges.

Tests must cover tenant separation, responsive behavior, keyboard/screen readers, contrast, revision conflicts, error rendering, permissions, CSRF and XSS resistance. Cosmetic changes may apply immediately; TLS domains and sensitive integrations follow Q47 with plan/recovery.

**State: design only; no working visual editor or dynamic widget runtime is shipped.**
