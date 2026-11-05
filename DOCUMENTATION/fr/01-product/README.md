<!-- forgepanel-doc id=FP-01 revision=6 status=documented -->
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

## Qualification et protection du MVP Q141–Q147

Le premier site PHP/HTTPS sera qualifié par **VM locales/cloud et rapports CI communs**, avec charge/performance par classe d'application, sécurité et régressions de versions (Q141/Q142). Le parcours de domaine à **DNS externe** propose les enregistrements attendus puis revérifie A/AAAA/80/HTTP-01/HTTPS sans modification automatique (Q143). Mises à jour OS contrôlées **par serveur** (Q144), backup **chiffré local avec clé récupérable** et destination distante facultative, KMS externe/multi-autorités seulement en option (Q145), SFTP sans shell/expiration/quotas/audit (Q146). Après tests internes, bêta privée avec critères de santé configurables, suspension des vagues et récupération (Q147). Les fonctions commerciales Q148–Q150 restent après ABI Hub. [Décisions Q141–Q150](../00-project-control/decisions-q141-q150.md). **Non livré aujourd'hui.**

## MVP : mise en pratique Q151–Q158

**QEMU/KVM local** devient le premier pilote de qualification, avec CI VM seulement si elle sait l'exécuter et possibilité de pilotes cloud ultérieurs (Q151). Les preuves sont **signées, historisées, internes** avec snapshots (Q152) ; les budgets/régressions de performance sont administrables et exceptions possibles **hors veto sécurité** (Q153). Le diagnostic DNS/HTTP-01 du premier domaine contrôle **les familles IP A/AAAA réellement publiées** (Q154), les reboots OS sont **approuvés par serveur** avec backup/santé/reprise (Q155). Un backup chiffré local ne sera déclaré récupérable qu'après vérification périodique des clés de secours et **restauration isolée réelle** (Q156). Le gestionnaire de site gérera ses **clés publiques SFTP** avec expiration/quotas/audit (Q157). La bêta privée prend en compte la santé locale et des diagnostics **minimisés sous consentements distincts** et seuils par cohorte (Q158). [Décisions](../00-project-control/decisions-q151-q160.md).

## Maîtrise du périmètre

Les fondations Core sont obligatoires ; les modules de services natifs sont sélectionnables sans dépendre de plugins tiers. Les plugins enrichissent les capacités, mais ne fournissent pas les garanties fondamentales de sécurité. Les recettes installent les applications clientes ; elles ne sont ni des modules Core ni des extensions privilégiées.

Le propriétaire a maintenant validé **un Core complet gratuit avec services/extensions premium et support payant (Q2)**, la double licence à finaliser (Q1), les catalogues officiels/partenaires vérifiés (Q8) et 60 jours de tolérance hors ligne pour les droits premium concernés (Q7). Les tarifs, l'essai, les conditions commerciales, l'application des droits et les anciennes règles WCP360 ne sont pas présumés. Voir la [politique produit](../00-project-control/product-policy.md). La réussite se mesure au fonctionnement et à la récupération vérifiés, pas au nombre d'écrans.

[Catalogue des modules](../04-modules/README.md) · [Priorités](../00-project-control/status.md)
