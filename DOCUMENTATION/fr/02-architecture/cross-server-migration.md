<!-- forgepanel-doc id=FP-02-XSERVER revision=1 status=specified -->
# Migration de site entre serveurs — plan, compatibilité et récupération

[English](../../en/02-architecture/cross-server-migration.md) · [Cycle du site](website-lifecycle.md) · [Décisions Q91–Q100](../00-project-control/decisions-q91-q100.md)

## Objectif Q100 D

Un administrateur autorisé peut planifier la **migration ou restauration d'un site entre deux serveurs ForgePanel**, avec ou sans création d'un staging isolé. L'origine et la destination doivent être reconnues, leur propriétaire vérifié, et le transfert autorisé **dans les deux périmètres**. Aucun accès root général ni commande shell arbitraire n'est fourni. Les ressources de production, emails, backups et données personnelles ne doivent pas être expédiés au Hub.

## Découverte, préflight et capacités

Garder une matrice versionnée : OS/architecture, espace et quotas, compte Unix/UID, DNS/ACME, IP/ports/listeners, WebStack et règles `.htaccess`, PHP/versions/extensions/FPM et contraintes d'isolation, bases MariaDB/MySQL/PostgreSQL, Redis/Valkey facultatifs, stockage persistant, cron/jobs, SSH/SFTP, mailboxes et certificats. Afficher les **incompatibilités bloquantes**, différences réparables et dépendances manquantes ; ne pas créer automatiquement de compte sur un serveur qui ne peut garantir l'isolation.

## Pipeline de migration

1. **DISCOVER/AUTHORIZE** : source et cible identifiées, clés/identités agent vérifiées, propriétaire/permissions, périmètre des données, consentement et durée de transfert.
2. **PLAN/PREVIEW** : compatibilité et risque, fenêtre de maintenance, taille estimée et coût, transfert/destruction possible, stratégie DNS/TLS et contacts clients, version des politiques.
3. **SNAPSHOT** : capture cohérente source/cible, données SQL à l'instant identifié, journaux et secrets protégés ; si possible, dernier backup restaurable avant interruption.
4. **TRANSFER** : canal authentifié/chiffré avec intégrité/empreintes, reprises idempotentes, quotas, rate-limits et aucun passage par le Hub commercial.
5. **STAGING/ADAPT** : nouveaux identifiants OS/app, secrets tournés et ACL, PHP/DB/WebStack compatibles, URLs, DNS de test et jobs sortants arrêtés, anonymisation/retention selon politique du site.
6. **VERIFY** : test HTTP/TLS/.htaccess, PHP et SQL, application, mail, quotas, restaurabilité, absence de fuite réseau et capacité de reprendre les services.
7. **CUTOVER** : bascule DNS/proxy ou frontend lorsque autorisée, avec avertissements TTL, propagation, sessions, nouveaux emails et écritures concurrentes. Si la cohérence ne peut être garantie, imposer une fenêtre de maintenance ou refuser la migration.
8. **COMMIT/RECOVER** : confirmer ownership, journal/révision/état, sauvegarde source et nettoyage à échéance ; en échec, proposer la restauration explicite et signaler les effets non réversibles.

Les opérations à forte incidence respectent Q47. Une migration de schéma SQL ou l'envoi de mails tiers ne peut pas être annulé par simple rollback de configuration. Une réplication bidirectionnelle active de données applicatives n'est **pas** décidée par Q100.

## Garanties de sécurité

- Protéger **les secrets d'origine** ; régénérer clés et tokens nécessaires côté cible, sans exporter les clés privées SSH/TLS par défaut.
- Résoudre les risques d'écrasement cible, permissions de fichiers/symlinks et DB user mapping avant plan d'application.
- Les environnements staging ne déclenchent ni emails de production, ni paiements, ni callbacks vers services externes, ni indexation publique sans action autorisée.
- Garantir la séparation du service PostgreSQL du Core et des moteurs SQL clients.
- Les copies durables suivent Q65/Q75 (chiffrement, stockage distant, immutabilité, 3-2-1 et tests).
- Les migrations entre serveurs déconnectés ou non certifiés nécessitent une procédure d'import sécurisée revue, **pas** une promesse de prise en charge universelle.

## Critères de validation (non exécutés)

Deux VM autorisées avec OS et WebStacks différents, transfert interrompu après snapshot, refus d'accès à une source tierce, changement PHP non compatible, espace insuffisant, DB en cours d'écriture, DNS non propagé, rotation et restauration des clés, contrôle des emails sortants, doublons de job et bascule avec statut inconnu. Vérifier à la fois les données et l'absence de régression des sites voisins.

**Statut : spécifié. Aucun moteur de migration inter-serveurs, double-commit, cluster ou restauration live n'existe actuellement.**
