<!-- forgepanel-doc id=FP-11-VISUAL revision=2 status=specified -->
# Éditeur visuel du Panel, widgets et navigation (Q70 D)

[English](../../en/11-design-system/visual-editor.md) · [Design system](README.md) · [Décisions](../00-project-control/infrastructure-decisions.md)

## Décision produit et limites

L'interface cible est **100 % Symfony** : Twig, Symfony UX Live Components, Stimulus, Turbo et Tailwind (outillage frontend léger). Le propriétaire a retenu un **éditeur visuel de mise en page**, des widgets configurables, une navigation personnalisable, l'aperçu et l'historique. Selon Q55 A, **une seule marque par organisation** ; on peut utiliser différents layouts/périmètres au sein de cette marque, pas créer plusieurs identités distinctes.

## Q80 — widgets officiels, partenaires et déclaratifs

Le catalogue cible permet les widgets **officiels et partenaires approuvés** plus des **widgets personnalisés déclaratifs** : composition de données existantes autorisées, filtres/agrégations bornés, graphiques et mises en page, sans interprétation de scripts libres. Le manifeste précise le propriétaire, les champs et ressources accessibles, les permissions RBAC, la version du schéma, la fréquence/limite des requêtes et le comportement en cas d'indisponibilité. Le simple affichage d'une source ne donne aucun droit de lecture nouveau. L'éditeur conserve une marque par organisation (Q55). [Décision Q80](../00-project-control/decisions-q71-q80.md).

## Modèle de personnalisation

Déclarer des `ThemeTokens`, `BrandAssets`, `Layout`, `DashboardWidget`, `NavigationItem`, `MenuSection` et `Localization` versionnés. Chaque composant déclare ID stable, version/contrat de rendu, props validées, permissions, rôle/périmètre, priorité et état de compatibilité. Les routes accessibles sont enregistrées par le Core ou des plugins approuvés. Masquer une entrée de menu **ne donne ni retire** l'autorisation effective du serveur.

Profils cibles : Admin, User, revendeur, collaborateur ; modes Standard/Advanced/Expert modifient l'ergonomie, jamais le RBAC. L'organisation peut régler logo, favicon, palette, typographie autorisée, domaine, identité des emails, widgets et menus dans la politique supérieure, sans afficher les secrets ni les données de tenants tiers.

## Éditeur et publication

`DRAFT → PREVIEW (ordinateur/mobile) → VALIDATE (contraste, accès, schéma) → PUBLISH (version et audit) → REVERT`. L'éditeur propose glisser/déposer, déplacement, tri, tailles de grille, visibilité et paramètres de widgets **autorisés**. Il ne fournit pas un exécuteur de PHP/JS/CSS non fiables ; les contenus HTML et URLs sont filtrés et échappés. Aucun widget de plugin non approuvé ne dispose d'un accès privilégié.

Les essais exigent isolation entre organisations, responsive, clavier/lecteur d'écran, contraste, conflits de version, rendu d'erreurs, permissions, CSRF et résistance XSS. Les changements peuvent être immédiats quand purement visuels ; les domaines/TLS et intégrations sensibles suivent Q47 (plan et récupération).

**Statut : conception, aucun éditeur visuel ni composant dynamique opérationnel aujourd'hui.**
