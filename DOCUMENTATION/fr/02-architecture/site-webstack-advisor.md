<!-- forgepanel-doc id=FP-02-SITE-WEBSTACK revision=2 status=specified -->
# Conseiller WebStack par site et changement de profil sécurisé

[English](../../en/02-architecture/site-webstack-advisor.md) · [Architecture](README.md) · [Arbitrages Q71–Q80](../00-project-control/decisions-q71-q80.md)

## Décision propriétaire — Q79 D, précisée

**À la création de chaque site**, ForgePanel calcule une ou plusieurs WebStacks **recommandées pour ce site** selon les besoins déclarés et capacités réellement détectées. Le panneau affiche une recommandation, ses motivations et alternatives admissibles. L'administrateur peut **accepter ou sélectionner un autre profil** compatible.

**Après création**, la page du site permet de **demander un changement de WebStack** à tout moment, avec vérification des autorisations, prévisualisation et plan de transition. Le choix ne devient effectif qu'après tests ; aucun basculement aveugle, garantie de zéro interruption ou modification de tous les sites du serveur.

## Décisions Q81 C et Q82 D — compatibilité et transition

Le conseiller Q81 **doit** tenir compte de la présence de règles `.htaccess`, des versions/extensions PHP, de l'OS, de l'isolation du compte, des contraintes de sécurité, des ressources/quotas et de la propriété des listeners IP:port. Les profils non compatibles sont refusés, et la recommandation est **propre à chaque site**, conformément à Q79.

Pour le changement d'un site, Q82 autorise une **route temporaire de test** ou une **bascule progressive uniquement lorsque l'infrastructure le permet**, après prévisualisation, sauvegarde, validation et gestion d'une fenêtre de maintenance/notification. Les cookies, sessions, écritures applicatives et fichiers protégés doivent rester cohérents. Sinon le système doit annoncer un cutover potentiellement interrompu. Aucun autre site partageant 443 ne doit changer de frontal par effet de bord. [Cycle du site](website-lifecycle.md).

## Critères de recommandation (futurs)

Entrées : OS/paquets réellement installables, frontaux et listeners disponibles (IP/port/TLS), PHP version et extensions demandées, application et ses règles, besoin `.htaccess`, compatibilité CGI/rewrites/auth, exigences de sécurité, isolation du compte, mode worker FrankenPHP admissible, profil et quotas d'hébergement. Chaque facteur a provenance et version de règle, affiche « disponible », « non compatible », « installation requise » ou « vérification manquante ». Ne pas prétendre mesurer une performance non benchmarkée.

Profils existants dans la spécification : `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp`. **Strict Nginx→Apache** route les requêtes couvertes par `.htaccess` vers Apache. Le mode accéléré avec fichiers statiques Nginx requiert politiques d'accès équivalentes au premier frontal ; ne jamais cacher un contournement de contrôle d'accès. `nginx_fpm`/Caddy direct n'interprètent pas `.htaccess`. Mode worker FrankenPHP limité aux applications et tenants vérifiés.

## Contrat de recommandation

Requête proposée : `webstack.recommend(site_draft,server_facts,policy_revision)`. Résultat : liste ordonnée de `profile_id`, `eligibility`, `reasons`, `warnings`, `required_components`, `listener_plan`, `confidence_evidence`, `estimated_impact`, `policy_revision`. Les raisons sont explicables et une impossibilité doit bloquer un choix, pas seulement afficher un avertissement. Les scores ne garantissent pas une performance supérieure.

Toute sélection requiert permission RBAC et **validation explicite**. La politique de serveur peut interdire un profil au client/revendeur même si techniquement compatible ; les capacités ne remplacent pas l'autorisation.

## Transition d'un site existant

1. **INVENTORY** : état courant, origine et propriétaire des fragments de configuration, listeners, versions PHP, TLS, document root, réécritures, règles d'accès, caches et jobs.
2. **PLAN/PREVIEW** : comparer ancien/nouveau profil, dépendances, installation de paquets requise, ports occupés, impacts sécurité et interruption potentielle. Déterminer s'il faut changer de frontal ou seulement de runtime/routage.
3. **VALIDATE** : permissions, quotas, capacités OS, disponibilité IP:port, syntaxe, compatibilité `.htaccess`, PHP et application ; refuse si validation manquante.
4. **SNAPSHOT** : préserver génération ForgePanel précédente, fichiers et données utiles lorsqu'une opération les modifie ; documenter les limites de récupération.
5. **STAGE** : préparer configurations séparées, pools et routes ; conserver les listeners du panneau et les autres sites ; config test avant activation.
6. **CUTOVER/VERIFY** : basculer la route ou le listener **selon topologie**, tester HTTP(S), TLS, PHP, contrôle d'accès et santé applicative. Un listener public partagé a un seul propriétaire ; si le frontal actuel est partagé, le changement d'un site ne doit pas remplacer celui des autres.
7. **COMMIT/RECOVER** : conserver la génération active, l'état d'opération, l'audit et une procédure de restauration/compensation. Un changement de code/app ou schéma SQL peut ne pas être réversible.

Modèle d'état cible : `RECOMMENDED → SELECTED → PLANNED → VALIDATING → STAGING → SWITCHING → VERIFYING → ACTIVE`, ou `FAILED/RECOVERING/MANUAL_INTERVENTION`. Jobs idempotents, verrou par site/listener, dérive et traces de diagnostic expurgées. Le certificat et la route de secours du panneau restent disponibles.

## Tests d'acceptation avant disponibilité

- Nouveau site PHP simple : liste des cinq profils filtrée par capacités sans fausse promesse ; recommandations expliquées et modifiables.
- Site utilisant `.htaccess` avec autorisations : refuser un profil direct incompatible ou afficher un plan complet de migration des règles contrôlé ; aucun bypass Nginx sur statiques sensibles.
- Migration d'un site entre Nginx/Apache et Caddy sur IP/ports admissibles : pas de conflit et pas d'impact sur un autre vhost.
- Changement avec TLS, PHP version/extensions et jobs en cours ; refus de permissions et plan obsolète ; timeout, interruption après snapshot, récupération.
- Frontal unique partagé sur 443 et plusieurs profils backend : routage testé et contrôle du propriétaire ; aucun remplacement implicite de l'ingress.
- Production de recommandations indépendantes par site, pas une simple préférence globale ; maintien du compte/quotas/secret.

**Statut : spécifié seulement. Aucun moteur de conseil, changement de WebStack en ligne ou validation VM n'est actuellement présent dans le Core.**
