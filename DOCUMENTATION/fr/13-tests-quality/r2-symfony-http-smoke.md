<!-- forgepanel-doc id=FP-13-R2-HTTP-SMOKE revision=3 status=specified -->
# R2 — Tests Symfony HttpKernel et contrôles Origin/CSRF

[English](../../en/13-tests-quality/r2-symfony-http-smoke.md) · [Matrice R2](r2-integration-gates.md) · [Tests PostgreSQL R2](r2-postgres-execution.md)

## Périmètre

Cette proposition empilée démarre le **véritable HttpKernel Symfony** à partir des sources Foundation R1, au lieu de confondre la vérification syntaxique ou un test PHP autonome avec une application Web en fonctionnement. Elle dépend de l'import R1 (#59), de la MFA facultative (#60) et des tests PostgreSQL jetables (#61). Aucun déploiement, port réseau ouvert, reverse proxy, connexion permanente ou installateur privilégié n'est autorisé.

Une CI GitHub éphémère installe les dépendances Symfony 7.4 et Twig 3 épinglées dans `composer.lock`, vérifie le routeur et le conteneur de services, puis envoie de **vraies requêtes HTTP Symfony dans le noyau**. Les assertions portent sur GET `/setup` réussi, le refus de HTTP non chiffré, un Host étranger, un mauvais port administrateur, une méthode inconnue, un POST d'origine étrangère, un corps trop volumineux ou un CSRF absent, ainsi que les en-têtes `no-store` et de sécurité. PostgreSQL n'est ici qu'une **base jetable** nécessaire à l'injection PDO.

## Preuves et limites

Une CI réussie donne une **preuve partielle du périmètre HTTP Symfony** pour le commit exact, pas une certification R2. Le verrou Composer candidat est maintenant **versionné dans cette PR brouillon** ; aucun dossier `vendor/`, vrai secret ou clé de signature n'est commité. La revue indépendante des licences et de la sécurité des dépendances, la compatibilité PHP/OS et les tests réels d'installation/récupération restent des **bloqueurs de release**.

Ne sont **PAS TESTÉS** : POST CSRF valide depuis un navigateur, échange de vrai jeton d'activation en HTTP, TLS signé / reverse proxy réel, connexion permanente, persistance de session navigateur, RBAC complet, création de site, agent privilégié, mise à jour de production, restauration ou machines virtuelles. Le reste de la matrice R2 demeure ouvert.

Le code `SetupBoundary` conserve un contrôle strict d'origine HTTPS et n'accorde aucune confiance aux en-têtes de proxy fournis par le client. Un reverse proxy réel nécessite une qualification distincte Security/DevOps. Ne pas dégrader les protections Host/Origin pour réussir un test. Le Core doit toujours fonctionner sans le Hub.

## Défaut de bootstrap découvert par la première CI

La première CI Symfony a échoué dans `config/bootstrap.php` : l’ancien `Dotenv::bootEnv()` tentait de lire un `.env` local absent, malgré les variables explicitement fournies par le workflow. Il s’agit d’un défaut réel de configuration R2, pas d’un problème PostgreSQL. La correction ne charge `.env` **que s’il existe**, conserve la priorité du fichier protégé `/etc/forgepanel/panel.env` et refuse toujours le démarrage si `APP_SECRET` manque ou est trop court. Aucun secret n’est lu dans `.env.example`. La [CI réelle Symfony #42384745856](https://github.com/yyogas/forgepanel/actions/runs/42384745856) a vérifié les corrections environnement/DI, le routage et 12 assertions HTTP sur le commit précédent. La nouvelle révision avec verrou épinglé doit encore passer ses contrôles indépendamment.

## Dépendances candidates épinglées — 07/11/2026

Après la première CI réelle Symfony réussie, le fichier `composer.lock` a été récupéré depuis l'artefact `13578779233`, vérifié octet par octet (SHA-256 `b1f9e5104c2749acc4fabaddb6a24e094f309c0a38d81f8af8cc7dda20204b68`). Il contient **47 packages**, sans plugin Composer, avec licences MIT/BSD-3-Clause déclarées ; `symfony/framework-bundle` est épinglé sur `v7.4.23`. Le verrou figure désormais dans la branche de PR proposée et la CI utilise `composer install`, non une résolution dynamique. La revue juridique complète et la compatibilité PHP/OS multi-cibles restent ouvertes. Ce verrou candidat n'est ni un binaire publié ni une autorisation de déploiement.