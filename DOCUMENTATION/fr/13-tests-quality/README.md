<!-- forgepanel-doc id=FP-13 revision=3 status=documented -->
# Tests, qualité et définition de terminé

[English](../../en/13-tests-quality/README.md) · [Index](../README.md)

## Une preuve précise son périmètre

Un compte rendu identifie commit/empreinte d'archive, outils, environnement, commande, résultat et limites non testées. `SKIP` n'est pas `PASS`. Les [preuves de vérification](../19-audits-risks/verification.md) distinguent réexécution SRC-03, validation documentaire et intégrations non exécutées.

| Couche | Preuve présente | Prochain critère |
|---|---|---|
| Prototype Go | Six packages testés, détecteur de courses et vet | Répéter sur le commit importé ; choisir le compilateur maintenu de publication |
| Métier PHP setup | Lanceur spécifique : 28 tests / 184 assertions | Compléter refus/récupération ; ne pas appeler cela PHPUnit |
| Syntaxe | Lint PHP sur 26 fichiers/points d'entrée | Vérifier framework/conteneur/templates réels |
| PostgreSQL | Source du test disponible | Rollback, concurrence, redémarrages et restauration sur base réelle |
| HTTP/navigateur | Protections/templates dans le code seulement | HTTPS, CSRF, sessions, origines, limites et E2E |
| Six OS / cinq profils | Logique de sélection sur fixtures | Matrice VM jetables : installation, upgrade, réinstallation, panne/reprise |
| Documentation | Vérificateur et lecture bilingue | Liens relatifs, métadonnées parallèles, contenu non vide, détection limitée de secrets |

PHPUnit, Go testing, Playwright, Bats, analyse statique et outils de charge restent la cible qualité selon les besoins. Leur recommandation ne prouve pas l'existence des pipelines. Docker seul ne remplace pas les VM pour services et sécurité Linux.

## Porte de sortie de la première version Q119 B

Une première livraison fonctionnelle exige un **test complet sur VM autorisée** : installation depuis artefact vérifié, setup initial avec choix MFA facultatif, connexion administrateur permanente, PostgreSQL réel, création d'un site PHP, validation de domaine, certificat HTTPS valide, requête HTTPS, droits RBAC, diagnostic et restauration d'une configuration en panne. Tester aussi échec de TLS, conflit IP:port et autorisation refusée. Nommer OS, WebStack, commit et résultats exacts ; ne pas assimiler des fixtures Go, tests PHP en mémoire ou CI documentaire à une certification d'hébergement. [Roadmap Q120 D](../00-project-control/implementation-roadmap.md).

## Porte de qualification révisée (Q121–Q127)

Avant de qualifier le **premier OS / la première WebStack**, comparer les VM et profils candidats avec critères de sécurité, paquets, PHP, listeners, HTTP/TLS et récupération (Q121/122). Tester DNS **externe**, challenge HTTP-01 sur **port 80**, serveur HTTPS et échecs DNS/IPv6/ports (Q123). Valider rôles admin/gestionnaire de site, récupération locale, sessions/CSRF et MFA facultatif (Q124), plans/autorisations/audit et reprise des mises à jour OS (Q125), et **restauration réelle** de configuration panneau + fichiers PHP avec état PostgreSQL cohérent si requis (Q126). Après ces résultats, la **bêta privée** est possible seulement avec conditions légales de diffusion et canaux sécurité vérifiés (Q127). [Matrice MVP](../00-project-control/mvp-qualification.md). **Aucun de ces tests d'intégration n'a été exécuté par cette PR.**

## Définition de terminé

Les critères passent au bon niveau ; refus et récupération sont testés ; compatibilité données/API et rollback sont consignés ; les deux langues et le changelog sont actualisés ; les preuves correspondent exactement au changement ; risques et vérifications manquantes sont visibles. La publication ajoute ses propres critères et une promotion autorisée.

Une revue de sécurité distincte est nécessaire avant les fonctions sensibles de production. Ce lot documentaire comporte une auto-revue de l'auteur, pas un second agent indépendant ni un audit externe. L'égalité des métadonnées ne prouve pas celle du sens ; la lecture sémantique bilingue reste nécessaire.
