<!-- forgepanel-doc id=FP-01 revision=4 status=documented -->
# Périmètre produit et parcours

[English](../../en/01-product/README.md) · [Index](../README.md)

## Utilisateurs et frontières

ForgePanel cible propriétaires de serveurs, hébergeurs, agences, revendeurs et clients d'hébergement. Ces profils sont des cibles produit ; seul l'enrôlement de l'administrateur initial est prototypé dans SRC-03. Le propriétaire du projet exprime ses besoins en langage naturel et n'assure ni l'implémentation ni la revue technique.

## Parcours exigés

| ID | Parcours | Critère d'acceptation |
|---|---|---|
| REQ-001 | Installer avec une commande | Sur VM vierge prise en charge, vérifier origine/signatures, prérequis, services isolés du panneau et accès HTTPS vérifié ; interruption et relance ne corrompent pas l'état |
| REQ-002 | Prendre possession de l'installation | Une preuve locale privilégiée émet un jeton court à usage unique ; créer un compte indépendant, proposer le MFA facultatif (activable maintenant ou plus tard) et fermer l'inscription initiale |
| REQ-003 | Configurer avec un wizard reprenable | Expliquer dépendances et changements système ; conserver l'avancement ; valider le plan avant application ; aucune réussite ambiguë après échec partiel |
| REQ-004 | Héberger sans plugins de marketplace | Compte, domaine, runtime PHP, TLS, base/fichiers et sauvegarde natifs fonctionnent avec des permissions explicites |
| REQ-005 | Diagnostiquer et récupérer localement | Diagnostic en lecture seule sans interface web ; réparation prévisualisée, bornée, auditée et préservant les données externes |
| REQ-006 | Proposer plusieurs OS/profils web | Annoncer uniquement les combinaisons individuellement testées ; ne pas proposer comme fonctionnel un profil indisponible |

L'archive s'arrête au brouillon de configuration revu, pas à la fin d'une installation. DNS, certificats, mail, gestion de fichiers, fonctions revendeur et provisionnement des services ne sont pas implémentés.

## Arbitrages infrastructure Q61–Q70

L'expérience cible combine installation universelle vérifiée, profils web et DNS/mail modulaires, sauvegardes distantes avec restauration, administration multi-serveurs à terme, monitoring et éditeur visuel. **Hébergement + VPS restent la première priorité** (Q54), sans prétendre livrer immédiatement la HA complète. MFA facultatif et une marque par organisation sont conservés. Voir [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Parcours d'hébergement Q81–Q90

La cible prévoit un site personnalisable : **WebStack recommandée par site, modifiable plus tard**, PHP-FPM/extensions et limites propres, certificats ACME/wildcards, Git Deploy/staging, moteurs MariaDB/MySQL/PostgreSQL avec Redis/Valkey facultatifs, fichiers/SFTP/SSH limité, webmail/quarantaine, plans/alertes et restauration sélective/clonage staging. Le changement de WebStack utilise une route temporaire ou une bascule progressive **si les capacités le permettent**, sans garantie zéro interruption. [Contrat Q81–Q90](../00-project-control/decisions-q81-q90.md). Aucune implémentation annoncée.

## Premier site PHP/HTTPS et bêta privée — Q121–Q127

La première expérience fonctionnelle cible **un site PHP avec domaine sous DNS externe et HTTPS ACME HTTP-01**, sans exiger de DNS natif. Les premiers OS et profil WebStack seront **choisis après comparaison des tests VM**, pas définis par défaut. Elle inclut administration locale + rôle gestionnaire de site, diagnostic VPS et mises à jour OS **contrôlées**, sauvegarde du panneau et des fichiers du site **avec restauration testée**. Une bêta privée ne suit qu'après tests internes et vérification des conditions de distribution et du signalement de sécurité. Tous ces parcours sont **à construire**. [MVP](../00-project-control/mvp-qualification.md).

## Maîtrise du périmètre

Les fondations Core sont obligatoires ; les modules de services natifs sont sélectionnables sans dépendre de plugins tiers. Les plugins enrichissent les capacités, mais ne fournissent pas les garanties fondamentales de sécurité. Les recettes installent les applications clientes ; elles ne sont ni des modules Core ni des extensions privilégiées.

Le propriétaire a maintenant validé **un Core complet gratuit avec services/extensions premium et support payant (Q2)**, la double licence à finaliser (Q1), les catalogues officiels/partenaires vérifiés (Q8) et 60 jours de tolérance hors ligne pour les droits premium concernés (Q7). Les tarifs, l'essai, les conditions commerciales, l'application des droits et les anciennes règles WCP360 ne sont pas présumés. Voir la [politique produit](../00-project-control/product-policy.md). La réussite se mesure au fonctionnement et à la récupération vérifiés, pas au nombre d'écrans.

[Catalogue des modules](../04-modules/README.md) · [Priorités](../00-project-control/status.md)
