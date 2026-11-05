<!-- forgepanel-doc id=FP-02-Q141-150 revision=1 status=specified -->
# Certification VM, budgets, sauvegarde, accès et mises à jour — Q141–Q147

[English](../../en/02-architecture/certification-backup-security.md) · [Décisions Q141–Q150](../00-project-control/decisions-q141-q150.md) · [Qualification MVP](../00-project-control/mvp-qualification.md)

## Pilotes de VM et preuves communes (Q141 D)

Contrat candidat `QualificationDriver` : `capabilities`, `provisionDisposableVM`, `snapshot`, `restoreSnapshot`, `injectFailure`, `collectEvidence`, `destroy`. Pilotes **VM locales** et **cloud** interchangeables, sans qu'un produit ou fournisseur soit imposé. Les runners CI doivent démontrer qu'ils peuvent réellement exécuter systemd, un kernel Linux, gestion des paquets, firewall et SELinux/AppArmor lorsque pertinent. Un job ignoré/indisponible doit être signalé `SKIP`, jamais « certifié ».

Un `QualificationReport` versionné rassemble identifiant d'image, OS/arch/version, profil WebStack, version Go/Symfony/PHP, commit et signatures, configuration des ressources, suite de tests, résultats individuels, logs expurgés, échec d'injection réseau/disque/reboot et **preuve de restauration**. Publier le rapport avec son périmètre exact ; pas d'affirmation de support pour un OS qui n'a pas passé les tests.

## Performances comparables et critères éliminatoires (Q142 D)

Définir profils de workloads par **type d'application** : PHP simple, application transactionnelle/CMS quand disponible et tests adaptés aux moteurs WebStack. Fixer et rapporter charge, environnement VM, versions, type de requêtes, durée, métriques de latence (médiane, p95/p99), débit, erreurs, CPU/RAM, saturation, comportement après reload/incident. Les budgets sont **configurables et versionnés**, avec analyse des régressions à environnement comparable : ne pas fabriquer de scores ni de seuils acceptables.

Toujours **refuser** un candidat qui expose des fichiers protégés, contourne `.htaccess`, traverse les comptes, entre en collision sur les ports partagés, échoue au TLS ou n'a pas de reprise prouvée, même s'il gagne un benchmark. Aucun profil n'est sélectionné par défaut avant les preuves.

## Assistant DNS externe (Q143 C)

L'UI indique **les enregistrements attendus** pour l'IP/IPv6/listener du site, les zones et les erreurs constatées, puis permet de **revérifier** A/AAAA, la résolution IPv6, le port **80**, le chemin de challenge **HTTP-01**, l'accès HTTPS **443** et la correspondance certificat/nom. Les contrôles de politique et d'autorisation restent dans Core ; cette option **ne permet pas de modifier automatiquement les enregistrements** chez un fournisseur DNS. Les erreurs et les recommandations doivent être précises sans exposer le jeton ACME.

## Mises à jour OS par serveur (Q144 D)

`ServerUpdatePolicy` candidate : sources/paquets autorisés, plages de maintenance, classes sécurité/fonction, versions protégées, actions sensibles, demande d'approbation, `plan_hash`, sauvegarde/snapshot récupérable, état `PENDING → APPLYING → REBOOT_REQUIRED → VERIFYING → COMPLETED/RECOVERING`. La planification affiche impact, services dépendants, quotas et interruption éventuelle. Réviser et revérifier le plan à l'exécution ; ne pas transformer une décision UI en shell root. **Orchestration progressive multi-serveurs ultérieure** (Q67/Q77), non critère MVP.

## Chiffrement et accès aux clés de restauration (Q145 D)

Les sauvegardes Q126/Q135 couvrent **configuration du panneau et fichiers PHP**, et l'état PostgreSQL interne nécessaire au redémarrage peut imposer une stratégie cohérente séparée. Le moteur chiffre les archives, maintient manifestes/signatures d'intégrité et distingue **clé de données**, clé de chiffrement, coffre local et copie de secours **hors de la panne commune**. L'accès à la clé est protégé, limité aux rôles autorisés, journalisé et sujet à rotation. Une option future de **KMS externe** ou d'approbations **multi-autorités de récupération** (ex. plusieurs gardiens autorisés) peut être offerte avec quorum défini par politique et procédures de secours. Le Core gratuit ne dépend ni du Hub ni d'un service externe pour la restauration locale autorisée. Prévoir tests de disque perdu, clés indisponibles, restauration sur VM distincte et limite des sauvegardes seulement locales ; ne jamais promettre une récupération si toutes les clés ont disparu.

## SFTP borné, contrôlé et auditable (Q146 C)

Chaque identité SFTP a des sites/répertoires autorisés, méthode d'accès par **clé**, shell **interdit par défaut**, expiration/revocation et quotas réels ; les chemins, permissions Unix et symlinks sont validés côté service, pas uniquement par UI. Audit des connexions/refus et modifications sensibles sans secrets ; suspendre l'accès sans effacer les fichiers. Le rôle gestionnaire Q136 ne reçoit pas de permissions OS globales.

## Bêta et arrêt de vagues (Q147 C)

Une `BetaRolloutPolicy` enregistre cohortes invitées, canal/version signé, critères de santé **configurables** et seuils de suspension, bug/incident grave, autorité de pause/reprise et procédure de récupération. Une pause empêche les **nouvelles installations et mises à jour de la vague**, sans effacer les données ni détruire les droits de copies légalement obtenues. Les diagnostics sont **volontaires ou contractuellement minimaux** (Q6) et correctement expurgés, non requis pour faire fonctionner le Core. Le responsable sécurité et son suppléant Q130 coordonnent les avis si nécessaires.

## Critères de livraison

Exiger tests automatisés de refus RBAC, restauration VM et backup chiffré avec clé récupérée, détection de régression et seuil de sécurité, DNS mauvais/IPv6/challenge manquant, update interrompu et SFTP croisé. Les pilotes sont **des contrats proposés**, pas des implémentations existantes. Les journaux de tests ne prouvent pas la sécurité d'un système non exécuté.
