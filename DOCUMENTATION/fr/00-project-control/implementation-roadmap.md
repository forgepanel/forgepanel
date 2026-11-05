<!-- forgepanel-doc id=FP-00-EXECUTION revision=2 status=specified -->
# Roadmap technique de réalisation — décision Q120 D et MVP Q119 B

[English](../../en/00-project-control/implementation-roadmap.md) · [État officiel](status.md) · [Décisions Q111–Q120](decisions-q111-q120.md)

## Ordre approuvé du propriétaire

**Importer les sources → vérifier Symfony/PostgreSQL → construire et tester l'installateur → exploiter le premier site PHP/VPS → valider une API d'extension générique → développer/intégrer ForgePanel-Hub.**

Cette séquence **remplace les priorités implicites** qui laisseraient les modules premium/marketplace précéder un Core fonctionnel ; elle ne supprime pas les décisions Q1–Q110. Les étapes peuvent comporter des branches préparatoires en parallèle, mais **aucune phase dépendante ne peut être déclarée achevée avant la preuve de la précédente**. Toutes les étapes ci-dessous restent à exécuter ; les contrôles documentaires ne prouvent pas leur réalisation.

| Gate | Travail concret | Sortie vérifiable et conditions de refus |
|---|---|---|
| **R1 — Sources** | Import de l'archive Foundation v0.7 vérifiée, examen des différences avec le correctif MFA facultatif v0.7.1, provenance/hashes, licence marquée en attente | PR `features/* → develop`, structure Go/PHP importée sans secrets ni binaires générés, `make check`/Go race/vet/PHP et refus de `install apply` tant qu'il n'est pas sécurisé. Préserver la documentation bilingue et le changelog unique. Suivi : [issue #2](https://github.com/yyogas/forgepanel/issues/2), [MFA #6](https://github.com/yyogas/forgepanel/issues/6). |
| **R2 — Symfony/PostgreSQL** | Dépendances Composer résolues/verrouillées, runtime Symfony actif, connexion PDO/PG dédiée, setup initial et identité permanente ; option activer/ignorer MFA, CSRF/HTTPS/sessions | Tests HTTP et navigateur du wizard, accès admin, CSRF, origine, autorisation, MFA facultatif, reprise et PostgreSQL réels (rollback, concurrence, redémarrage, réponse perdue). Reproduire sur revision précise. Suivi : [issue #3](https://github.com/yyogas/forgepanel/issues/3). |
| **R3 — Installateur sûr** | Build Go, provenance/signatures, commande vérifiée, préflight, étapes idempotentes, systemd/logs/reprise. **Comparer les prérequis et essais VM des OS cibles avant de choisir le premier OS (Q121 D).** | Preuves comparatives install/upgrade/échecs/récupération, OS/version/commit ; **aucun OS prédéterminé** et aucune certification des six OS sans test distinct. [Qualification](mvp-qualification.md) · [issue #15](https://github.com/yyogas/forgepanel/issues/15). |
| **R4 — Site PHP et VPS minimum** | **Choisir la première WebStack après essais compatibilité/sécurité (Q122 D)** ; site PHP isolé avec domaine géré par **DNS externe**, ACME **HTTP-01** et HTTPS automatique (Q123 A) ; identité permanente et **rôles admin/gestionnaire de site** (Q124 B) ; surveillance VPS, logs, **opérations de paquets/mises à jour OS contrôlées** (Q125 B) ; **backup/restauration testés configuration du panneau + fichiers PHP** (Q126 B). | VM propre : install/wizard/login → site PHP/domaine/DNS externe → challenge HTTP sur port 80 → HTTPS réel → permissions refusées → paquet mis à jour avec plan/audit → backup et restauration réels. Le stockage PG indispensable au panneau exige une reprise cohérente. Aucune WebStack ni CA choisie d'avance. [Qualification](mvp-qualification.md) · [site #20](https://github.com/yyogas/forgepanel/issues/20) · [MVP #29](https://github.com/yyogas/forgepanel/issues/29). |
| **R5 — API neutre d'extension** | ABI versionnée pour services détachés, permission fine, cycle verify/stage/activate/disable/remove et plugin d'essai **non Hub** | Extension neutre signée fonctionne sur Core normal, est refusée si non fiable/incompatible, et son arrêt/suppression ne stoppe jamais les sites. Tests permissions/versions/rollback. Suivi : [issue #7](https://github.com/yyogas/forgepanel/issues/7). |
| **R6 — Hub après R5** | Symfony Hub isolé + PostgreSQL distinct, organisations, offres, paiement sandbox, licence/pools, catalogue officiel/partenaires, vérification des droits et distribution signée | Tests interopérabilité Core-Hub, client offline, webhooks signés/idempotents, transferts de licences, motif de révocation, confidentialité ; aucune nécessité du Hub pour la connexion ou la réparation du Core. Suivi : [dépôt Hub](https://github.com/yyogas/forgepanel-hub) et ses issues. |

**R4 est le périmètre de première version fonctionnelle Q119 B**. Les opérations R5/R6 sont **postérieures** à ce jalon. La cible Q54 reste hébergement mutualisé + administration VPS ; ne pas exiger cluster HA, Webmail, DNS local ou tous les langages avant la première démonstration. Le choix du **premier OS, WebStack et domaine de test** doit être étayé, non présumé ici.

## Extension Q121–Q130 : preuves MVP, bêta et responsabilités

**Q121 D / Q122 D :** sélectionner le premier couple OS/WebStack **uniquement à partir de comparatifs VM** ; aucune plateforme ni pile choisie par l'utilisateur. **Q123 A :** parcours v1 fondé sur DNS **externe** et validation ACME **HTTP-01**, sans exiger DNS natif ou DNS-01 au premier jalon. **Q124 B / Q125 B / Q126 B :** compte administrateur et gestionnaire de site, VPS supervisé avec gestion contrôlée des paquets, sauvegarde de config panneau et fichiers PHP avec restauration **réellement testée**. La [matrice de qualification](mvp-qualification.md) décrit les cas négatifs.

**Q127 B :** après tests internes isolés, une **bêta privée** limitée à des testeurs autorisés est possible seulement avec validation du propriétaire, canal sécurité opérationnel et conditions de licence/diffusion vérifiées **aussi pour ces destinataires externes** ; ce n'est pas une release publique ni un passe-droit juridique. Les Q128 D (licences transférables et récupération manuelle de serveur perdu), Q129 C (maintenance partenaires contractualisée/alertes/retrait) attendent le **Hub après ABI**. **Q130 C** demande un responsable sécurité et un suppléant **effectivement désignés**, triage et notifications coordonnées ; ne pas inventer leur identité ou un email.

## Contrôles transversaux et diffusion publique

Avant de déclarer une release utilisable : chaque environnement testé est nommé (OS/version, composants, commit, outils, statut), la sécurité de la connexion et du wizard est prouvée, les sauvegardes/restaurations réelles passent, et les défaillances sont consignées. Une CI documentaire ou des tests de domaine PHP ne remplacent pas HTTP, PostgreSQL et VM.

Avant **distribution publique** : conclure la revue juridique AGPL/commercial (Q111) et CLA électronique (Q112), droits des dépendances et politique de marque ; configurer et **vérifier** signalement privé GitHub + contact email sécurité (Q118) et procédures de triage. Ne pas inventer d'adresse, ne pas choisir de licence finale sans décision juridique. Les deux canaux de sécurité ne sont pas considérés ouverts avant vérification.

À chaque étape : branch `features/*`, PR ciblée vers `develop`, tests et preuves, revue quand disponible, mise à jour FR/EN et changelog ; promotions contrôlées ultérieurement vers `stable`, `main`, `production`, **jamais automatiques** sur une décision de documentation.

## Risques et dépendances

Le code Core n'est **pas encore importé** dans `develop` ; le prototype v0.7.1 MFA facultatif reste en archive séparée. Les intégrations Symfony/PG et l'installateur ne sont pas démontrés par les workflows actuels. Le plan ne promet pas de calendrier ou d'effet système immédiat. Toute revendication de progression doit être attachée à un commit, un test et un environnement vérifiables.
