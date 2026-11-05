<!-- forgepanel-doc id=FP-12 revision=2 status=documented -->
# Environnement et conventions de développement

[English](../../en/12-development/README.md) · [Index](../README.md)

## Travail disponible dans le dépôt

Ce lot contient la documentation et son vérificateur, pas les sources applicatives. À la racine, lancer `python3 scripts/check_documentation.py`. Python est seulement un outil documentaire ; le produit reste PHP/Go. Lire [AGENTS.md](../../../AGENTS.md) et le [relais](../18-contributing/handover.md) avant une tâche.

Code, identifiants, commentaires techniques, commits et chemins techniques sont en anglais. Les échanges propriétaire sont en français. Les documents officiels ont des équivalents avec mêmes ID/révisions ; tout retard de traduction précise périmètre et tâche de rattrapage. Ne pas recopier les règles normatives dans plusieurs fichiers racine.

## Développement de l'archive fournie

Après un import revu séparément, SRC-03 permet `go test ./...`, `go test -race ./...`, `go vet ./...`, `php apps/panel/tests/run.php`, `make build` et `bash scripts/check.sh`. Ces commandes ne sont pas disponibles à la racine actuelle du dépôt. Le lanceur PHP est spécifique, pas PHPUnit. Ces tests natifs exigent Sodium et Argon2id. Le manifeste requiert PHP >=8.2 et Symfony 7.4 ; `go.mod` déclare 1.23.0. Les versions du laboratoire ne définissent pas le support de publication.

Les dépendances Composer ne sont ni verrouillées ni installées dans l'archive. Les résoudre, examiner, verrouiller et auditer dans un environnement isolé sans contourner les prérequis. Ajouter les vérifications réelles du conteneur Symfony, YAML, Twig et routage avant exposition HTTP. Les tests PostgreSQL exigent une base dédiée autorisée ; jamais des identifiants de production.

## Frontières des changements

Séparer règles métier et contrôleurs, particularités OS et contrats du domaine. Définir types bornés et erreurs avant les opérations privilégiées. Ne pas importer de code tiers sans examen licence/provenance. Binaires générés, caches, vendor et secrets réels sont exclus du socle initial.

Un agent inspecte espace de travail et branches distantes, réutilise les branches pertinentes, évite les modifications concurrentes de fichiers partagés et laisse des preuves exactes. Un conteneur de développement ne certifie pas systemd, pare-feu, quotas ou politiques obligatoires sur les VM cibles.

## Admission R1 : outil de code vérifiable

L'utilitaire `scripts/verify_source_archive.py` vérifie en **lecture seule** l'archive originale SRC-03 avant import. Il compare son empreinte et son inventaire au registre, analyse le ZIP et génère un rapport JSON, sans exécuter ni installer de code. **16 tests unitaires utilisant uniquement des archives synthétiques** sont automatisés dans la CI. Le Core applicatif PHP/Go n'est toujours **pas importé**. [Contrat et mode d'emploi](source-archive-intake.md).
