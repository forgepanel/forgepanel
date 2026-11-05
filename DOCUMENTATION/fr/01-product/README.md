<!-- forgepanel-doc id=FP-01 revision=1 status=documented -->
# Périmètre produit et parcours

[English](../../en/01-product/README.md) · [Index](../README.md)

## Utilisateurs et frontières

ForgePanel cible propriétaires de serveurs, hébergeurs, agences, revendeurs et clients d'hébergement. Ces profils sont des cibles produit ; seul l'enrôlement de l'administrateur initial est prototypé dans SRC-03. Le propriétaire du projet exprime ses besoins en langage naturel et n'assure ni l'implémentation ni la revue technique.

## Parcours exigés

| ID | Parcours | Critère d'acceptation |
|---|---|---|
| REQ-001 | Installer avec une commande | Sur VM vierge prise en charge, vérifier origine/signatures, prérequis, services isolés du panneau et accès HTTPS vérifié ; interruption et relance ne corrompent pas l'état |
| REQ-002 | Prendre possession de l'installation | Une preuve locale privilégiée émet un jeton court à usage unique ; créer un compte indépendant, imposer le MFA et fermer l'inscription initiale |
| REQ-003 | Configurer avec un wizard reprenable | Expliquer dépendances et changements système ; conserver l'avancement ; valider le plan avant application ; aucune réussite ambiguë après échec partiel |
| REQ-004 | Héberger sans plugins de marketplace | Compte, domaine, runtime PHP, TLS, base/fichiers et sauvegarde natifs fonctionnent avec des permissions explicites |
| REQ-005 | Diagnostiquer et récupérer localement | Diagnostic en lecture seule sans interface web ; réparation prévisualisée, bornée, auditée et préservant les données externes |
| REQ-006 | Proposer plusieurs OS/profils web | Annoncer uniquement les combinaisons individuellement testées ; ne pas proposer comme fonctionnel un profil indisponible |

L'archive s'arrête au brouillon de configuration revu, pas à la fin d'une installation. DNS, certificats, mail, gestion de fichiers, fonctions revendeur et provisionnement des services ne sont pas implémentés.

## Maîtrise du périmètre

Les fondations Core sont obligatoires ; les modules de services natifs sont sélectionnables sans dépendre de plugins tiers. Les plugins enrichissent les capacités, mais ne fournissent pas les garanties fondamentales de sécurité. Les recettes installent les applications clientes ; elles ne sont ni des modules Core ni des extensions privilégiées.

Cette référence n'adopte aucun tarif, essai, serveur de licence, modèle économique de marketplace ou règle commerciale WCP360. Ces choix nécessitent des décisions produit séparées. La réussite se mesure au fonctionnement et à la récupération vérifiés, pas au nombre d'écrans.

[Catalogue des modules](../04-modules/README.md) · [Priorités](../00-project-control/status.md)
