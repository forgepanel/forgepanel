<!-- forgepanel-doc id=FP-02-Q101-110 revision=1 status=specified -->
# Politiques de runtime, de staging, d'accès et de continuité (Q101–Q110)

[English](../../en/02-architecture/runtime-exceptions-and-data-continuity.md) · [Arbitrages](../00-project-control/decisions-q101-q110.md) · [PHP et staging](php-staging-and-access-policy.md) · [Migration inter-serveurs](cross-server-migration.md)

## 1. PHP temporairement obsolète et isolation certifiée

Un `PHPVersionException` proposé référence `site_id`, version EOL, origine des paquets, motif, administrateur autorisant, date d'expiration, preuves, risques et `migration_plan_id`. La dérogation vaut uniquement pour le **site et la période approuvés**. Afficher des alertes, bloquer par politique de sécurité les nouvelles demandes incompatibles et imposer une nouvelle décision avant expiration. Ne pas désactiver l'hébergement ou effacer les données sans action explicite autorisée.

Un `SiteIsolationProfile` proposé déclare identités/sockets FPM, montages, quotas, capabilities cgroups, politiques SELinux/AppArmor/systemd et **matrice des OS certifiés**. Le responsable peut choisir parmi les profils autorisés à la fois par le plan et par les capacités réelles du serveur ; interdire un profil incomplet ou faux. Les exceptions PHP ne suspendent pas les autres contrôles d'isolation.

## 2. Environnement et approbation du déploiement Git

Chaque environnement d'un site (`production`, `staging` ou un environnement validé) porte sa propre `DeployPolicy` : modes `manual`/`webhook`, refs permises, secrets d'authentification, branche protégée, tests obligatoires, fenêtre de déploiement, droit de déclenchement et règle d'approbation. Une approbation Q76 est **configurable par action/environnement** ; elle ne transforme pas tous les déploiements staging en double validation obligatoire. Vérifier signature, timestamp et anti-rejeu avant d'enregistrer un job, et ne jamais interpréter un payload comme un programme shell root.

## 3. Staging contenant des données sensibles

Le profil `StagingCopyPolicy` précise `files_only`, `schema_only` ou `anonymized_data` (catégories proposées), et la classification des champs copiés. Les données sensibles nécessitent une **autorisation supplémentaire distincte**, journalisant demandeur, approbateur, portée, finalité et validité. Protéger contre les réidentifications, secrets transférés, copies de tokens, callbacks réels, email sortant, moteurs de recherche et accès non autorisé. Rétention bornée, purge et tests de suppression, avec exceptions légales/audit explicitement documentées.

## 4. Renouvellement ACME résilient

Un `AcmeIssuerAdapter` peut déclarer CA, méthodes de challenge, comptes, DNS-01, rate-limit et conditions de bascule. Le choix et les autorités alternatives doivent être **préalablement approuvés**. En cas d'échec : retries limités avec backoff et journal, alerte et escalade, conserver le dernier certificat valide jusqu'à confirmation d'un nouveau ; si aucune option sûre, générer un incident et une procédure manuelle de secours. Ne pas contourner la validation de domaine ni mettre une clé privée dans les logs.

## 5. Bases mutualisées, dédiées et clusters facultatifs

Le plan déclare `database_topology` : **mutualisé** (tenant/roles séparés) ou **dédié**, avec moteur et quotas permis. Clusters et réplication restent des **drivers optionnels certifiés**, non une conséquence automatique du choix de base. Spécifier cohérence, réplication, rôle principal, failover, sauvegardes et restauration par moteur. Redis/Valkey facultatifs n'obtiennent pas de port public ni d'accès aux DB voisins. Le PostgreSQL du panneau reste à part.

## 6. SSH temporaire, Webmail recommandé, dépassement de quota

`SSHAccessGrant` inclut utilisateur OS, clé ou certificat SSH de CA approuvée, IP autorisées, restrictions de chemin/commande, date de fin et révocation suivie d'un audit. Ne pas supposer les certificats SSH disponibles si aucun pilote/CA certifié n'existe. Pas de root générique ni de terminal web introduit par Q107.

Le moteur de recommandation Webmail classe seulement les pilotes réellement **maintenus, testés et compatibles** avec le serveur/fournisseur/domaine ; il explique critères et exigences de migration. Il ne choisit pas implicitement Roundcube ou SnappyMail.

`QuotaGracePolicy` est scoped par **plan et type de ressource** : plafond soft, limite hard, seuils, délai borné, notification, actor/grant d'extension Q99 et expiration. Les ressources ne deviennent pas illimitées pendant la grâce : refuser toute valeur dépassant capacités physiques et politiques de sécurité.

## 7. Pré-synchronisation et bascule avancée conditionnelle

Une migration peut utiliser `snapshot → presync → isolated staging → consistency/final sync → DNS/proxy cutover → verify`, avec logs, locks, compensation et RPO/RTO **mesurés**. Une réplication active/failover est autorisée **uniquement si moteur DB, application, stockage, topologie réseau et tests de cohérence la supportent**. Si des écritures ne peuvent être réconciliées, forcer une fenêtre de maintenance ou refuser la migration. La synchronisation répétée ne signifie pas transaction distribuée ni « zéro downtime ». [Détails du pipeline](cross-server-migration.md).

## Critères de sortie

Environnements de test OS et comptes isolés, tests réels du moteur des règles, scénarios d'échec/reprise, aucune divulgation de secrets, scripts/procédures de secours explicitement revus. Tous les API/types décrits sont **des propositions**, pas du code produit présent.
