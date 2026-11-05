<!-- forgepanel-doc id=FP-15 revision=5 status=documented -->
# Exploitation, diagnostic et récupération

[English](../../en/15-operations/README.md) · [Index](../README.md)

## Limite opérationnelle actuelle

Ce dépôt ne contient aucune instance ForgePanel déployée. La CLI SRC-03 fournit `doctor` en lecture seule, la planification et un pont console de setup conditionnel. `status`, `repair`, `services`, `webstack`, `admin`, `update` et `backup` ne sont pas des commandes opérationnelles complètes ; les opérations absentes refusent sans modifier le système. Ne pas demander à un opérateur de réparer la production avec elles.

## Récupération du setup prototype

Sur un prototype correctement installé à l'avenir, `sudo forgepanel setup status` consulte le setup ; l'émission de jetons/reprises exige terminal interactif et console Symfony fixe de confiance. PHP et PostgreSQL doivent fonctionner. Le binaire Go exécutable ne permet pas de récupérer un compte dépendant de SQL lorsque la base est arrêtée. Le jeton initial se régénère avant la création du compte ; après celle-ci, utiliser la reprise locale prévue sans rouvrir l'inscription initiale.

## Procédure d'incident cible

Noter symptômes, révision et ressource ; lancer un diagnostic non modifiant ; préserver logs expurgés et dernière configuration ; limiter l'exposition si nécessaire ; préparer une réparation bornée ; confirmer l'impact destructif ; appliquer sous verrous ; vérifier santé/récupération ; consigner résultat et risque restant. Ne jamais effacer les logs, désactiver la sécurité obligatoire ou écraser des configurations externes comme correction automatique.

Observer santé des services, ID d'opérations, durées, catégories d'échec, saturation, certificats et sauvegardes. Les métriques n'exposent ni secrets clients ni identifiants sensibles à forte cardinalité. Routage des alertes et rétention ne sont pas implémentés et nécessitent une configuration explicite.

## Conservation par catégorie (Q59)

Les audits de privilèges, logs système, jobs, métriques, diagnostics, sessions, sauvegardes, tickets et données commerciales Hub ont des politiques distinctes. Rétention, anonymisation, archive et purge configurables dans le cadre légal et sécuritaire ; aucune durée arbitraire fixée et aucun effacement des preuves requises pour incident ou restauration. [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

## Gestion avancée et supervision (Q65, Q67, Q68)

Sauvegardes chiffrées multi-destinations avec réplication et immutabilité, supervision locale et alertes email/webhooks/intégrations externes, et cible multi-serveurs/HA/DR. Chaque adaptation doit exposer quotas, consentement, rétention et opérations de récupération ; la disponibilité effective exige tests de restauration et de défaillance. Le clustering est à développer après la fondation. [Architecture](../02-architecture/service-drivers-and-ha.md).

## 3-2-1, observabilité et reprise (Q75, Q77, Q78)

Le profil de sauvegarde visé est **3-2-1**, avec tests de restauration planifiés, réplication et copie distante, selon capacités et budgets réels ; l'immutabilité Q65 reste une exigence de destination prise en charge. La supervision Q78 utilise des pilotes Prometheus/OpenTelemetry et des règles d'export autorisées. Q77 prévoit les agents distants en premier puis des modules HA/orchestrateurs optionnels : redondance, quorum et reprise exigent des essais, pas une simple case dans l'interface. [Référence](../00-project-control/decisions-q71-q80.md).

## Restauration sélective et staging (Q85/Q90)

Les sauvegardes de site devront permettre restauration complète ou sélective (fichiers/base/configuration), tests de restauration, clonage staging et transfert entre environnements **avec autorisation du propriétaire**. Avant tout écrasement : plan, vérification quotas/espace, snapshot de destination, séparation des secrets/URLs et contrôle de santé. Un déploiement Git et son retour au commit précédent n'annulent pas une migration SQL. Les échecs partiels exigent un état de récupération explicite. [Cycle du site](../02-architecture/website-lifecycle.md).

## Sauvegarde et restauration requises

Définir une couverture cohérente des configurations, métadonnées, fichiers clients, bases et clés de chiffrement. Tester la restauration isolément et mesurer durée/perte de données ; ne promettre aucun RPO/RTO avant mesure. La perte de clé peut rendre les données MFA irrécupérables. Le futur moteur sépare diagnostic, simulation et application, conserve l'ancien accès jusqu'à validation du nouveau et prévoit une issue de secours en cas d'interruption.

[Sécurité](../10-security/README.md) · [Qualité](../13-tests-quality/README.md)
