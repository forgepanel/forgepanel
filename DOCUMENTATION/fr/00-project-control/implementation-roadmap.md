<!-- forgepanel-doc id=FP-00-EXECUTION revision=1 status=specified -->
# Roadmap technique de réalisation — décision Q120 D et MVP Q119 B

[English](../../en/00-project-control/implementation-roadmap.md) · [État officiel](status.md) · [Décisions Q111–Q120](decisions-q111-q120.md)

## Ordre approuvé du propriétaire

**Importer les sources → vérifier Symfony/PostgreSQL → construire et tester l'installateur → exploiter le premier site PHP/VPS → valider une API d'extension générique → développer/intégrer ForgePanel-Hub.**

Cette séquence **remplace les priorités implicites** qui laisseraient les modules premium/marketplace précéder un Core fonctionnel ; elle ne supprime pas les décisions Q1–Q110. Les étapes peuvent comporter des branches préparatoires en parallèle, mais **aucune phase dépendante ne peut être déclarée achevée avant la preuve de la précédente**. Toutes les étapes ci-dessous restent à exécuter ; les contrôles documentaires ne prouvent pas leur réalisation.

| Gate | Travail concret | Sortie vérifiable et conditions de refus |
|---|---|---|
| **R1 — Sources** | Import de l'archive Foundation v0.7 vérifiée, examen des différences avec le correctif MFA facultatif v0.7.1, provenance/hashes, licence marquée en attente | PR `features/* → develop`, structure Go/PHP importée sans secrets ni binaires générés, `make check`/Go race/vet/PHP et refus de `install apply` tant qu'il n'est pas sécurisé. Préserver la documentation bilingue et le changelog unique. Suivi : [issue #2](https://github.com/yyogas/forgepanel/issues/2), [MFA #6](https://github.com/yyogas/forgepanel/issues/6). |
| **R2 — Symfony/PostgreSQL** | Dépendances Composer résolues/verrouillées, runtime Symfony actif, connexion PDO/PG dédiée, setup initial et identité permanente ; option activer/ignorer MFA, CSRF/HTTPS/sessions | Tests HTTP et navigateur du wizard, accès admin, CSRF, origine, autorisation, MFA facultatif, reprise et PostgreSQL réels (rollback, concurrence, redémarrage, réponse perdue). Reproduire sur revision précise. Suivi : [issue #3](https://github.com/yyogas/forgepanel/issues/3). |
| **R3 — Installateur sûr** | Build Go, provenance et signature de paquets, installation en une commande, plan, préflight, application idempotente, user/systemd/TLS, logs/backup/reprise | Installation propre sur **au moins un OS explicitement qualifié**, puis autres OS par matrice VM ; vérifier uninstall/reinstall/upgrade, échec à chaque étape, restauration et chemins de secours. Ne pas annoncer six OS certifiés sans tests. Suivi : [issue #15](https://github.com/yyogas/forgepanel/issues/15). |
| **R4 — Site PHP et VPS minimum** | Agent minimal, identité/RBAC locale, configuration sûre, un profil WebStack réellement qualifié, domaine, accès HTTP(S), PHP-FPM isolé et certificat valide ; administration VPS/diagnostic essentiels | Depuis un serveur propre : installateur → wizard → connexion admin → création et administration d'un **site PHP avec domaine + HTTPS** → requête HTTPS valide → contrôle de ressources et refus RBAC → backup de config et récupération d'un échec. Tests VM/HTTPS/ports/TLS/PHP/droits. Suivi : [site #20](https://github.com/yyogas/forgepanel/issues/20), [hébergement #22](https://github.com/yyogas/forgepanel/issues/22). |
| **R5 — API neutre d'extension** | ABI versionnée pour services détachés, permission fine, cycle verify/stage/activate/disable/remove et plugin d'essai **non Hub** | Extension neutre signée fonctionne sur Core normal, est refusée si non fiable/incompatible, et son arrêt/suppression ne stoppe jamais les sites. Tests permissions/versions/rollback. Suivi : [issue #7](https://github.com/yyogas/forgepanel/issues/7). |
| **R6 — Hub après R5** | Symfony Hub isolé + PostgreSQL distinct, organisations, offres, paiement sandbox, licence/pools, catalogue officiel/partenaires, vérification des droits et distribution signée | Tests interopérabilité Core-Hub, client offline, webhooks signés/idempotents, transferts de licences, motif de révocation, confidentialité ; aucune nécessité du Hub pour la connexion ou la réparation du Core. Suivi : [dépôt Hub](https://github.com/yyogas/forgepanel-hub) et ses issues. |

**R4 est le périmètre de première version fonctionnelle Q119 B**. Les opérations R5/R6 sont **postérieures** à ce jalon. La cible Q54 reste hébergement mutualisé + administration VPS ; ne pas exiger cluster HA, Webmail, DNS local ou tous les langages avant la première démonstration. Le choix du **premier OS, WebStack et domaine de test** doit être étayé, non présumé ici.

## Contrôles transversaux et diffusion publique

Avant de déclarer une release utilisable : chaque environnement testé est nommé (OS/version, composants, commit, outils, statut), la sécurité de la connexion et du wizard est prouvée, les sauvegardes/restaurations réelles passent, et les défaillances sont consignées. Une CI documentaire ou des tests de domaine PHP ne remplacent pas HTTP, PostgreSQL et VM.

Avant **distribution publique** : conclure la revue juridique AGPL/commercial (Q111) et CLA électronique (Q112), droits des dépendances et politique de marque ; configurer et **vérifier** signalement privé GitHub + contact email sécurité (Q118) et procédures de triage. Ne pas inventer d'adresse, ne pas choisir de licence finale sans décision juridique. Les deux canaux de sécurité ne sont pas considérés ouverts avant vérification.

À chaque étape : branch `features/*`, PR ciblée vers `develop`, tests et preuves, revue quand disponible, mise à jour FR/EN et changelog ; promotions contrôlées ultérieurement vers `stable`, `main`, `production`, **jamais automatiques** sur une décision de documentation.

## Risques et dépendances

Le code Core n'est **pas encore importé** dans `develop` ; le prototype v0.7.1 MFA facultatif reste en archive séparée. Les intégrations Symfony/PG et l'installateur ne sont pas démontrés par les workflows actuels. Le plan ne promet pas de calendrier ou d'effet système immédiat. Toute revendication de progression doit être attachée à un commit, un test et un environnement vérifiables.
