<!-- forgepanel-doc id=FP-19-VERIFICATION revision=1 status=documented -->
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
