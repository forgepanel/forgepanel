<!-- forgepanel-doc id=FP-19-VERIFICATION revision=7 status=documented -->
# Rapport de vérification

[English](../../en/19-audits-risks/verification.md) · [Index d'audit](README.md)

## Contrôles frais de l'archive source

Entrée : SRC-03, SHA-256 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`. Conteneur Linux amd64 ; Go 1.23.2 ; PHP CLI 8.4.24. Ce sont les versions réelles du laboratoire, pas des recommandations de publication. Les commandes s'exécutent hors du dépôt Git sur l'archive extraite de façon contrôlée, sans résolution réseau Go.

| Commande / contrôle | Résultat observé | Limite |
|---|---|---|
| Comparaison SHA-256 archive | PASS | Conforme à l'empreinte fournie, pas une signature d'éditeur de confiance |
| `bash scripts/check.sh` | Sortie 0 | Contrôles natifs de l'archive uniquement |
| `go test ./...` | Six packages réussis | Aucun service système installé |
| `go test -race ./...` | Six packages réussis | Tests exercés, pas preuve d'absence de toutes courses |
| `go vet ./...` | Réussi | Analyse de ces sources/outils |
| Syntaxe PHP | 26 fichiers/points d'entrée réussis | Syntaxe, pas exécution du framework |
| `php apps/panel/tests/run.php` | 28 tests, 184 assertions, 0 échec | Dépôt en mémoire |
| `make build`, version/plan CLI | Réussis | Exécutable local ; plan toujours non exécutable |
| `forgepanel install apply` | Sortie 64, refus attendu | Aucun moteur d'application de production |
| `php apps/panel/tests/postgres.php` | Sortie 77, SKIP | Aucun pilote PDO ; pas de base de test autorisée |

Les logs historiques de l'archive sont des preuves distinctes. Aucun démarrage Symfony, résolution/audit Composer, concurrence PostgreSQL, test navigateur, installation six OS, hébergement, provisionnement TLS ou benchmark n'est exécuté dans ce lot documentaire. Aucun binaire de production n'est publié.

## Contrôles documentaires

Le vérificateur contrôle 20 index par langue, chemins parallèles, ID/révisions/statuts, certains identifiants d'exigences partagés, liens relatifs, changelog unique, syntaxe JSON et quelques motifs de secrets. Il ne prouve ni équivalence sémantique des traductions, ni fonctionnement applicatif, ni absence de tout secret. L'auteur relit aussi sources/affirmations et deux langues ; aucune revue indépendante n'est revendiquée.

L'exécution réelle se consulte dans les contrôles et logs de la PR documentaire. Ajouter un workflow ne signifie pas réussir la CI. Tout échec ou contrôle ignoré reste visible dans le compte rendu et doit être corrigé ou explicitement consigné avant promotion.

## Preuves documentaires observées

La [PR nº 1](https://github.com/yyogas/forgepanel/pull/1), tête `04e75476fce679714429c62ac83897262b64fa45`, a réussi le [run Actions 41948356066](https://github.com/yyogas/forgepanel/actions/runs/41948356066) : 10 tests du vérificateur, 28 paires, 64 fichiers Markdown et 282 liens relatifs. GitHub a testé la prévisualisation temporaire de fusion `de3b954943728538e5bcfbb0d0b3351a0ea8db87` ; la PR n’était pas fusionnée. La copie téléchargée a réussi les mêmes contrôles localement.

Ce run réussi signalait que ses actions v4 figées ciblaient un runtime Node déprécié. Ce complément fige les commits officiels vérifiés utilisant Node 24 (checkout v7.0.1 et upload-artifact v7.0.2), sans augmenter les permissions du dépôt. Son résultat CI propre doit être vérifié sur la nouvelle tête de PR, pas déduit du run précédent.

## Vérification supplémentaire R1 : aucun SRC-03 réel re-testé

**Commande locale** : `python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v`. **Résultat mesuré** : 16 tests sur 16 PASS, sur Linux/Python stdlib, avec archives fictives. Tests de refus : SHA incorrect, archive absente, chemins absolus/Windows/traversée, symlinks, doublons, compte/taille/ratio, secrets reconnaissables. **L'archive source v0.7 n'était pas disponible** ; aucun Go/PHP, PostgreSQL, VM ni processus de restauration du produit n'a été exécuté ici. Les résultats CI sur le commit précis de la PR sont vérifiés séparément. [Outil](../12-development/source-archive-intake.md).

## Campagne supplémentaire — audit de fichiers en quarantaine

La campagne `tests/source_intake` couvre également l'outil indépendant `audit_staged_archive.py` : cas synthétiques positifs/négatifs de cohérence ZIP/reçu/disque, refus des liens, permissions, modifications, inventaire additionnel/supprimé et courses de nettoyage. **État de validation à lire sur l'exact commit de la PR et sur le commit post-fusion**, sans inférer de résultats de CI antérieurs. Aucune vraie archive Foundation, aucun Core exécuté ni OS certifié. [Contrat](../12-development/source-staging-audit.md).

**Extension R1 (PR #39) :** 60 tests unitaires synthétiques exécutés avec succès sur les outils préflight/quarantaine/audit. Les contrôles négatifs couvrent notamment la modification de contenu de taille identique et différente, la substitution de dossier pendant nettoyage, les liens, les modes exécutables et les reçus falsifiés. Aucun runtime Foundation, Postgres, VM ou sauvegarde réelle n'a été testé. [CI de vérification](https://github.com/yyogas/forgepanel/actions/runs/42108723238).

## Campagne R3 : admission d'image QCOW2

**Preuve CI de la PR #41** : [Go + Go race + vet + gofmt + contrôle des trois schémas](https://github.com/yyogas/forgepanel/actions/runs/42116200478) et [contrôles documentaires](https://github.com/yyogas/forgepanel/actions/runs/42116200493), réussis sur le commit `4a71d2fb8e0258879bcf5c621dfc29677f5e5380`. **41 fonctions de tests Go** dans le module au total (14 sonde hôte et 27 nouveaux contrôles image/CLI/contrats) ; fixtures QCOW2 synthétiques, pas de VM réellement démarrée, ni de preuve de signature/isolement.

Ce succès ne valide aucun pilote QEMU/KVM, aucune VM isolée, quotas effectifs ou Core Foundation importé.

## Registre de preuves R3 — contrats candidats uniquement

La [matrice R3](../13-tests-quality/r3-ipc-installer-gates.md) et les [schémas IPC candidats](../08-api-contracts/symfony-go-ipc-r3.md) font l'objet de vérifications **statiques** Python (parité FR/EN, identifiants, aucune action shell libre, deux opérations privilégiées bloquées). Résultat réel de la CI : à associer au SHA précis après exécution. **Aucun** `R3-IPC-TEST-001..012` ou `R3-INSTALL-TEST-001..012` n'a été réalisé sur un agent, socket, installateur ou VM. Les preuves des anciennes PR R1/R3 ne certifient pas ce nouveau protocole. Aucune revue de sécurité indépendante n'est déclarée.
