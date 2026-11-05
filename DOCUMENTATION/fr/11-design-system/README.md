<!-- forgepanel-doc id=FP-11 revision=1 status=documented -->
# Design system et internationalisation

[English](../../en/11-design-system/README.md) · [Index](../README.md)

## Identité établie

Produit : **ForgePanel — The Modern Linux Server Control Panel**. Signature : **Modern • Secure • Modular • Scalable**. Aucun logo validé, palette, licence de police ou bibliothèque visuelle complète n'est établi. Les anciennes maquettes illustratives ne sont pas des interfaces livrées.

La référence frontend est Twig avec Symfony UX/Stimulus et Turbo/Live Components de manière sélective. SRC-03 contient les templates Twig du setup et `public/assets/setup.css`, pas un design system Tailwind/UX déployé. Préserver cette distinction pour les dépendances et la compilation des assets.

## États d'interaction requis

Tout composant d'action distingue repos, chargement, réussite, vide, erreur de validation, permission refusée, interruption et échec partiel. Un job en file n'est pas terminé. Afficher changements et ressources touchées avant une opération sensible ; éviter la réparation irréversible en un clic. Le wizard conserve l'avancement et distingue brouillon revu et configuration appliquée. Les erreurs techniques portent une référence de corrélation sans exposer de secrets.

Prévoir libellés explicites, navigation clavier, focus visible, erreurs compréhensibles, états indépendants de la couleur et responsive. Tester contraste, zoom et lecteur d'écran avant toute affirmation d'accessibilité. Une capture d'écran ne suffit pas à valider fonctionnement ou sécurité.

## Stratégie d'internationalisation

Cible : clés de traduction stables en anglais dans les catalogues Symfony, messages français/anglais, dates/nombres localisés et repli documenté. Valeurs de protocole, ID d'opération et codes de logs restent neutres. Ne pas traduire permissions ou clés de schéma. Les textes littéraux des templates SRC-03 sont un prototype, pas une infrastructure de traduction achevée.

Chaque écran exige les deux langues, textes longs, petit écran, états d'accès refusé et vérification de l'absence de secrets. Langues produit et tokens graphiques de production restent à spécifier ; ce chapitre n'introduit aucun nouveau framework frontend.

[Interfaces](../07-interfaces-roles/README.md) · [Qualité](../13-tests-quality/README.md)
