<!-- forgepanel-doc id=FP-13 revision=25 status=documented -->
# Tests, qualité et définition de terminé

[English](../../en/13-tests-quality/README.md) · [Index](../README.md)

## App Center : tests de séparation des origines fictives

La [frontière de confiance du préflight](../10-security/app-center-admission-trust-boundary.md) distingue désormais **trois jeux de données de test** (ressources Linux, droits Core, intention du client). Les [39 tests d'aperçu hors ligne](../../../tests/documentation/test_app_center_preview.py) couvrent champs non autorisés, références hôte/tenant falsifiées, faux statuts VERIFIED, gratuité native sans Docker/Hub et ports réservés. Aucun contrôle RBAC réel, attestation hôte ou installation n'est testé.

## App Center : contrôles de prévisualisation synthétique

Le [prototype d'aperçu non exécutable](../08-api-contracts/app-center-preview-contract.md) et les [tests négatifs hors ligne](../../../tests/documentation/test_app_center_preview.py) contrôlent la séparation des moteurs, les budgets fictifs CPU/RAM/PIDs, les sites non autorisés et les ports réservés 8447/8446. Aucun listener, hôte, droit réel ni installation n'est testé ; les 32 tests HTTP/VM restent PLANNED.

## App Center : manifestes candidats versus tests réels

Les [tests hors ligne des recettes](../../../tests/documentation/test_app_center_recipe_contracts.py) vérifient seulement des JSON synthétiques et refusent certains champs dangereux, **sans installer de logiciel**. Les [32 tests applicatifs/VM](app-center-engine-gates.md) restent PLANNED ; aucun OS ou moteur Docker/Podman n'est certifié par la CI statique.

## App Center : tests natifs et conteneurs distincts

La [matrice APP-NAT / APP-CTR / APP-X](app-center-engine-gates.md) prévoit **32 tests** : moteur natif gratuit, séparation Docker/Podman, ressources/quota/backup propres, refus des recettes inter-moteurs, isolation tenant, Hub absent et sécurité des artefacts. Tous sont **PLANNED**, aucun test d'installation applicative réelle n'a été exécuté. [Règles produit](../06-apps-recipes/app-center-engines.md).

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

## Règles supplémentaires de certification Q131–Q132

Automatiser les matrices de **VM système** locales et CI, conserver snapshots, injecter pannes et générer **rapports OS/versions/WebStack/commit** avec résultats par scénario. La preuve inclut le retour arrière des configurations et les exceptions `SKIP`, non comptées comme tests réussis. **WebStack initiale** : comparer charge réellement mesurée, sécurité d'isolation et `.htaccess`, maintenance/reload, TLS/ports et récupération ; **bloquer tout profil** ayant collision de port, fuite de données ou défaut de récupération, même si ses benchmarks sont meilleurs.

## Tests MVP de DNS, OS, sauvegarde et rôles Q133–Q136

Tester A/AAAA (IPv4/IPv6), port 80, routage HTTP-01, domaine externe et HTTPS 443 ; mises à jour OS avec plan d'impact/backup/health/recovery, y compris coupure et reboot ; copies **locales chiffrées** panneau+PHP avec restauration réelle, clé de déchiffrement disponible et destination distante **optionnelle** ; refus RBAC du gestionnaire de site sur les paquets OS, autres sites, dépassement de quota et sauvegardes tierces. [Matrice détaillée](../00-project-control/mvp-qualification.md). **Aucun test de ce type n'est exécuté par cette PR documentaire.**

## Tests comparables Q141–Q143 et SFTP Q146

**Q141 D** : les pilotes VM locales/cloud et les runners CI fournissent un rapport **commun** (OS/version/architecture/commit/WebStack, résultats par scénario, snapshots, simulations d'échec et preuve de restauration). Ne jamais marquer `SKIP` comme `PASS` ni présenter un conteneur comme VM Linux complète.

**Q142 D** : définir un **budget par type d'application** et une référence de version, contrôler débit, erreurs, latences, CPU/mémoire et régressions sur infrastructure comparable. Les **critères éliminatoires** Q132 (sécurité `.htaccess`, isolation, TLS, ports, récupération) priment sur toute performance. Pas de chiffres supposés.

**Q143 C** : vérifier suggestions d'enregistrements DNS puis recontrôler A/AAAA/IPv6, 80/HTTP-01, 443/HTTPS et certificat **après correction manuelle**, sans requérir des droits d'édition DNS fournisseur.

**Q145 D/Q146 C** : déchiffrer une sauvegarde en VM différente avec clés de secours réellement disponibles ; simuler perte du coffre/serveur et panne de KMS facultatif. Vérifier SFTP sans shell, chemin cantonné, expiration/révocation, quotas, refus inter-tenants et audit réel. [Matrice Q141–Q150](../00-project-control/decisions-q141-q150.md). **Aucun résultat de VM n'est ajouté par le seul changement documentaire.**

## Qualification Q151–Q156 — refus et preuves

Le premier pilote d'essai est **QEMU/KVM local** (Q151 A). Un runner qui ne peut pas démarrer une vraie VM retourne `SKIP`/`BLOCKED` et non une certification. Les rapports ont **signature/intégrité, provenance OS/image/commit, snapshots et historique de scénarios** (Q152 C) ; la matrice demeure interne tant que sa publication n'est pas autorisée. Tester les **budgets par application** et les régressions de versions (Q153 C) : une dérogation de performance est **approuvée, bornée et auditée**, jamais un contournement des veto de sécurité Q132. Pour HTTP-01, vérifier **seulement les familles A/AAAA effectivement publiées**, **toutes** celles présentes, sans échec fictif d'une IPv6 non configurée (Q154 C). Reboot OS par politique serveur et sauvegarde/santé/récupération Q155. Déclarer un backup chiffré « récupérable » **uniquement après export protégé de la clé, vérification périodique d'accès et restauration isolée réussie** (Q156 C) ; tester coffre/serveur indisponible. [Décisions](../00-project-control/decisions-q151-q160.md).

## Définition de terminé

Les critères passent au bon niveau ; refus et récupération sont testés ; compatibilité données/API et rollback sont consignés ; les deux langues et le changelog sont actualisés ; les preuves correspondent exactement au changement ; risques et vérifications manquantes sont visibles. La publication ajoute ses propres critères et une promotion autorisée.

Une revue de sécurité distincte est nécessaire avant les fonctions sensibles de production. Ce lot documentaire comporte une auto-revue de l'auteur, pas un second agent indépendant ni un audit externe. L'égalité des métadonnées ne prouve pas celle du sens ; la lecture sémantique bilingue reste nécessaire.

## Traçabilité de qualification Q151–Q160

La [matrice des tests positifs et négatifs](mvp-gates-q151-q160.md) définit les cas **MVP-Q151-01 à MVP-Q160-01**, avec statut initial **PLANNED**, jalon R3/R4/bêta/Hub et preuves exigées. Priorités : VM KVM réelle, rapport interne signé, exceptions performance sans contournement Q132, vérification HTTP-01 par familles IP publiées, reboot par serveur, restauration isolée avec contrôle des clés, SFTP à clés publiques, consentements distincts, risque premium et avis signés bilingues/structurés. Le nouveau test Python vérifie l'existence et la parité des cas, **pas l'exécution des services**.

## Matrice QA Q161–Q170

[Les dix cas MVP-Q161-01 à MVP-Q170-01](mvp-gates-q161-q170.md) sont **PLANNED**, avec chemin positif, refus négatif, phase R3/R4/bêta/Hub et preuves attendues. Les cas bloquants incluent fuite de secret runner, rapport signé altéré, dérogation critique Q132, sonde SSRF, récupération OS non bornée, backup sans restauration isolée, algorithme SFTP interdit, cohorte réidentifiable, transfert premium suspect et avis JSON/FR/EN incohérents. Un test Python statique vérifie décisions/ADR/couverture bilingue ; **pas de test matériel, Linux ou restauration réelle**.

## Tests réels de l'outil de préflight R1 (et limites)

`python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v` : **16 tests unitaires locaux PASS**, sur ZIP fictifs seulement. Cas : archive saine, SHA erroné, fichier absent, chemins dangereux, collisions, symlink, quotas/ratio, `.env`, indicateur de clé privée, nombre de membres et preuve source. Leur ajout au workflow CI ne certifie ni l'archive originale SRC-03, ni Go/PHP, ni PostgreSQL/HTTP/VM/restore. [Procédure de provenance](../12-development/source-archive-intake.md).

## Tests synthétiques R1 étendus — 33 scénarios

La [quarantaine de provenance](../12-development/source-staging.md) et le préflight R1 sont désormais couverts par **33 tests synthétiques** : 16 vérifications ZIP existantes, 6 refus supplémentaires (Unicode trompeur, `.git`, modes privilégiés, variantes `.env`) et 11 cas staging (mode lecture seule, destination privée/permissions, refus root et remplacement, preuve personnalisée bloquée pour `--stage`, modification d'archive détectée/nettoyée). Commande CI : `python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v`. **Ces résultats ne prouvent ni import réel de SRC-03 ni exécution applicative**.

## Contrôles négatifs d'intégrité après staging — R1

Nouvelle suite `tests/source_intake/test_audit_staged_archive.py` et cas complémentaires dans `test_stage_source_archive.py`. Elle teste **sans archive réelle** la cohérence ZIP/reçu/fichiers, les liens symboliques et physiques, les dossiers ou fichiers ajoutés/manquants, les permissions excessives, les reçus invalides et les substitutions concurrentes de dossier pendant un échec de staging. [Spécification](../12-development/source-staging-audit.md). La CI doit exécuter tous les tests du répertoire `tests/source_intake` sur le SHA final. Un succès ne garantit ni R1 importé, ni SQL/HTTP, ni VM ou restauration.

**Campagne sur la branche PR #39 : 60 tests R1 synthétiques réussis**. Le rapport CI exact du commit de PR reste l'autorité ; l'archive historique de l'issue #2 n'a pas été accessible ni contrôlée. Aucune affirmation de conformité production.

## Tests Go de l'observation KVM — lot préparatoire R3

Le module séparé [KVM Host Probe](../14-devops-releases/kvm-host-probe.md) possède **14 tests Go synthétiques** : périphérique KVM caractère/absent/faux/symlink, drapeaux VMX/SVM exacts, autres architectures, erreurs de lecture, données OS filtrées et **interdiction de fausse qualification**. Son workflow dédié exécute `go test ./...`, `go test -race ./...`, `go vet ./...` et vérifie que le JSON réel conserve `qualification=NOT_EXECUTED`. **Le runner GitHub n'est pas un hôte KVM certifié ; les VMs, snapshots, pannes, quotas, sauvegardes et restaurations réelles restent PLANNED.**

## R3 — Tests d'admission d'images QCOW2 sans VM réelle

Les tests Go synthétiques de `tools/kvm-host-probe/admission` et du CLI valident l'empreinte SHA-256, le nom du fichier, les permissions privées, le refus symlink/hardlink/format erroné, les plafonds explicites, l'interdiction réseau/partage/privilèges et la parité des trois JSON Schema. Le workflow Go existant exécute **`go test ./...`, `go test -race ./...`, `go vet ./...` et `gofmt`** ; le verdict de la PR doit être lu au SHA exact. Les fixtures ne sont pas des Linux démarrables, et aucun essai KVM, quota imposé, snapshot, rapport signé ou restauration n'est démontré. [Contrat](../14-devops-releases/kvm-image-admission.md).

**Preuve CI de la PR #41** : [Go + Go race + vet + gofmt + contrôle des trois schémas](https://github.com/yyogas/forgepanel/actions/runs/42116200478) et [contrôles documentaires](https://github.com/yyogas/forgepanel/actions/runs/42116200493), réussis sur le commit `4a71d2fb8e0258879bcf5c621dfc29677f5e5380`. **41 fonctions de tests Go** dans le module au total (14 sonde hôte et 27 nouveaux contrôles image/CLI/contrats) ; fixtures QCOW2 synthétiques, pas de VM réellement démarrée, ni de preuve de signature/isolement.

## R3 — Tests de copie privée vérifiée

La nouvelle suite de tests Go de [staging d’images](../14-devops-releases/kvm-image-staging.md) contrôle la copie identique SHA-256, les permissions 0700/0400, le refus d’écrasement, symlinks, chemins imbriqués ou partagés, demandes non autorisées, modifications de la source, interruptions et absence de reçu sur copie partielle. Le CLI est testé avec et sans fichiers de politique/demande privés ; le schéma du reçu est comparé aux champs Go. **62 fonctions de test Go au total dans le module**, et exécution locale réussie de `go test ./...`, `go test -race ./...`, `go vet ./...`. CI GitHub par SHA à vérifier ; **aucun boot QEMU ou test de quotas réels**.

## R2 — Matrice HTTP, MFA facultative et PostgreSQL

La [matrice R2](r2-integration-gates.md) ajoute **20 scénarios planifiés** : `R2-AUTH-001..010` et `R2-DB-TEST-001..010`, chacun avec parcours positif et refus/récupération négatif. Les fiches [identité](../03-core/bootstrap-identity-r2.md) et [transaction SQL](../09-database/setup-transaction-r2.md) restent candidates ; **aucun de ces 20 tests n'a été exécuté** sur Symfony/PostgreSQL par ce lot. Les contrôles Python de documentation vérifient seulement couverture et parité FR/EN.

## R3 — Matrice IPC et installateur : 24 tests non exécutés

La [matrice R3](r3-ipc-installer-gates.md) ajoute `R3-IPC-TEST-001..012` et `R3-INSTALL-TEST-001..012`, **24 scénarios positifs/négatifs au statut `PLANNED`**. Une validation Python statique contrôlera les IDs, la parité FR/EN, les deux JSON Schema candidats et le [registre fermé](../../evidence/typed-agent-operations-v1.json). **Aucun test réel Symfony↔Go, système Linux, installateur, PostgreSQL ou VM n'est exécuté par cette matrice.**

## R3 — 24 cas jobs durables / pair IPC à réaliser

La [matrice R3](r3-jobs-peer-gates.md) ajoute **R3-JOB-TEST-001..012** et **R3-PEER-TEST-001..012**, tous PLANNED. Scénarios : commit avant ACK, clé identique/digest différent, fencing périmé, worker crash/reprise et état Linux incertain ; usurpation d'UID/PID, socket remplacé, séparation du compte bridge, contrôle tenant/role indépendant, saturation et version incompatible. Les schémas JSON et tests Python vérifient uniquement la **cohérence documentaire** ; aucune DB de production, socket réel, VM ou autorisation système exécutée.

## R3 — Nouvelle matrice physique/identités/exécution, uniquement planifiée

La [matrice QA physique R3](r3-physical-execution-gates.md) décrit **36 cas PLANNED** `R3-PHYS-TEST-001..012`, `R3-LINUX-TEST-001..012` et `R3-EXEC-TEST-001..012`. Les tests Python de documentation contrôlent les 8 objets SQL candidats, 8 identités Linux, 7 opérations typées, veto des 2 handlers root et parité FR/EN. **Aucune base PostgreSQL réelle, séparation Linux ni effet systemd n'est exécuté** par ce lot ; les QA VM/HTTP/DB restent à prouver sur hôte autorisé.

## R3 — Huit nouveaux tests négatifs après revue d'intégrité

La [revue R3 des jobs](../19-audits-risks/r3-job-integrity-audit.md) ajoute `R3-AUDIT-TEST-001..008` **PLANNED** pour admissions refusées sans job, fencing après suppression/restauration, crash inbox avant/après effet et falsification tenant/RLS. `tests/documentation/test_r3_job_integrity_review.py` vérifie **uniquement les gardes documentaires** et leur non-régression par mutation d'objets JSON en mémoire. **Zéro test réel PostgreSQL/Linux** ; pas de résolution automatique des RISK-033..036.
