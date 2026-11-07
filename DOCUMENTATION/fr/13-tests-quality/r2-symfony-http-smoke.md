<!-- forgepanel-doc id=FP-13-R2-HTTP-SMOKE revision=2 status=specified -->
# R2 — Tests Symfony HttpKernel et contrôles Origin/CSRF

[English](../../en/13-tests-quality/r2-symfony-http-smoke.md) · [Matrice R2](r2-integration-gates.md) · [Tests PostgreSQL R2](r2-postgres-execution.md)

## Périmètre

Cette proposition empilée démarre le **véritable HttpKernel Symfony** à partir des sources Foundation R1, au lieu de confondre la vérification syntaxique ou un test PHP autonome avec une application Web en fonctionnement. Elle dépend de l'import R1 (#59), de la MFA facultative (#60) et des tests PostgreSQL jetables (#61). Aucun déploiement, port réseau ouvert, reverse proxy, connexion permanente ou installateur privilégié n'est autorisé.

Une CI GitHub éphémère résout Symfony 7.4 et Twig 3 avec Composer, vérifie le routeur et le conteneur de services, puis envoie de **vraies requêtes HTTP Symfony dans le noyau**. Les assertions portent sur GET `/setup` réussi, le refus de HTTP non chiffré, un Host étranger, un mauvais port administrateur, une méthode inconnue, un POST d'origine étrangère, un corps trop volumineux ou un CSRF absent, ainsi que les en-têtes `no-store` et de sécurité. PostgreSQL n'est ici qu'une **base jetable** nécessaire à l'injection PDO.

## Preuves et limites

Une CI réussie donne une **preuve partielle du périmètre HTTP Symfony** pour le commit exact, pas une certification R2. La résolution Composer est *temporaire* : ce lot ne versionne pas encore `composer.lock`, aucun vendor ni vrai secret dans Git public. Le verrouillage/audit des dépendances, leur provenance et la reproductibilité complète restent des **bloqueurs de release**. Un futur `composer.lock` épinglé doit être créé, revu et commité séparément avant toute annonce de production.

Ne sont **PAS TESTÉS** : POST CSRF valide depuis un navigateur, échange de vrai jeton d'activation en HTTP, TLS signé / reverse proxy réel, connexion permanente, persistance de session navigateur, RBAC complet, création de site, agent privilégié, mise à jour de production, restauration ou machines virtuelles. Le reste de la matrice R2 demeure ouvert.

Le code `SetupBoundary` conserve un contrôle strict d'origine HTTPS et n'accorde aucune confiance aux en-têtes de proxy fournis par le client. Un reverse proxy réel nécessite une qualification distincte Security/DevOps. Ne pas dégrader les protections Host/Origin pour réussir un test. Le Core doit toujours fonctionner sans le Hub.

## Défaut de bootstrap découvert par la première CI

La première CI Symfony a échoué dans `config/bootstrap.php` : l’ancien `Dotenv::bootEnv()` tentait de lire un `.env` local absent, malgré les variables explicitement fournies par le workflow. Il s’agit d’un défaut réel de configuration R2, pas d’un problème PostgreSQL. La correction ne charge `.env` **que s’il existe**, conserve la priorité du fichier protégé `/etc/forgepanel/panel.env` et refuse toujours le démarrage si `APP_SECRET` manque ou est trop court. Aucun secret n’est lu dans `.env.example`. La CI Symfony réelle doit être relancée avant toute validation de ce correctif.