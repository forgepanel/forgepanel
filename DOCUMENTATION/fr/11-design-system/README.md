<!-- forgepanel-doc id=FP-11 revision=4 status=documented -->
# Design system et internationalisation

[English](../../en/11-design-system/README.md) · [Index](../README.md)

## Identité établie

Produit : **ForgePanel — The Modern Linux Server Control Panel**. Signature : **Modern • Secure • Modular • Scalable**. Aucun logo validé, palette, licence de police ou bibliothèque visuelle complète n'est établi. Les anciennes maquettes illustratives ne sont pas des interfaces livrées.

La référence frontend est Twig avec Symfony UX/Stimulus et Turbo/Live Components de manière sélective. SRC-03 contient les templates Twig du setup et `public/assets/setup.css`, pas un design system Tailwind/UX déployé. Préserver cette distinction pour les dépendances et la compilation des assets.

## Isolation des interfaces FORGE et PANEL

La cible conserve deux surfaces avec préfixes, ports, sessions et assets séparés : **FORGE `/forge` : 8447** et **PANEL `/panel` : 8446**, avec hôtes HTTPS 443 configurables. Chaque espace dispose de son header, de sa sidebar et de ses variables de thème propres ; des composants réutilisables restent soumis à leurs contrats et aux permissions. Les bundles CSS/JS sont isolés pour éviter collisions et chargements non autorisés. Les maquettes n'apportent ni route active, ni isolation RBAC. [Contrat d'accès](../07-interfaces-roles/portal-access-routing.md) · [Tests planifiés](../13-tests-quality/portal-access-gates.md).

## États d'interaction requis

Tout composant d'action distingue repos, chargement, réussite, vide, erreur de validation, permission refusée, interruption et échec partiel. Un job en file n'est pas terminé. Afficher changements et ressources touchées avant une opération sensible ; éviter la réparation irréversible en un clic. Le wizard conserve l'avancement et distingue brouillon revu et configuration appliquée. Les erreurs techniques portent une référence de corrélation sans exposer de secrets.

Prévoir libellés explicites, navigation clavier, focus visible, erreurs compréhensibles, états indépendants de la couleur et responsive. Tester contraste, zoom et lecteur d'écran avant toute affirmation d'accessibilité. Une capture d'écran ne suffit pas à valider fonctionnement ou sécurité.

## Stratégie d'internationalisation

Cible : clés de traduction stables en anglais dans les catalogues Symfony, messages français/anglais, dates/nombres localisés et repli documenté. Valeurs de protocole, ID d'opération et codes de logs restent neutres. Ne pas traduire permissions ou clés de schéma. Les textes littéraux des templates SRC-03 sont un prototype, pas une infrastructure de traduction achevée.

Chaque écran exige les deux langues, textes longs, petit écran, états d'accès refusé et vérification de l'absence de secrets. Langues produit et tokens graphiques de production restent à spécifier ; ce chapitre n'introduit aucun nouveau framework frontend.

Q70 D ajoute un [éditeur visuel de thèmes, layouts, widgets et navigation](visual-editor.md), toujours basé sur Symfony Twig/UX ; Q55 A limite à **une identité de marque par organisation**. Les composants doivent être validés, accessibles et permissionnés, sans code JavaScript/PHP arbitraire. Ce n'est pas encore implémenté.

Q80 confirme les **widgets officiels et partenaires approuvés**, complétés par des **widgets déclaratifs personnalisés** avec sources de données autorisées, contrôle de paramètres et droits. Un widget n'est pas un script PHP/JS exécutable libre ; rester sur Symfony/Twig/UX et une marque par organisation. Voir [éditeur visuel](visual-editor.md) et [Q71–Q80](../00-project-control/decisions-q71-q80.md).

[Interfaces](../07-interfaces-roles/README.md) · [Qualité](../13-tests-quality/README.md)
