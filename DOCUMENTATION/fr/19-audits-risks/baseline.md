<!-- forgepanel-doc id=FP-19-BASELINE revision=1 status=documented -->
# Audit initial et provenance

[English](../../en/19-audits-risks/baseline.md) · [Index d'audit](README.md)

Date : 2026-11-05. Périmètre : dépôt connecté `yyogas/forgepanel`, conversation projet visible et pièces jointes sources montées. Aucun autre échange, serveur externe ou service privé n'a été supposé accessible.

## Constats du dépôt avant modification

Le connecteur résout le dépôt et indique visibilité privée et droits de lecture/écriture. L'endpoint de contenu renvoie `This repository is empty` ; celui des commits `Git Repository is empty` ; branches, issues, PR et releases sont vides. Actions indique total_count=0. Aucun code, workflow ou fichier de consignes ne pouvait donc être lu dans un arbre du dépôt.

La lecture des rulesets renvoie HTTP 403 avec une exigence de formule/visibilité. Après initialisation, la protection de main renvoie HTTP 403 `Resource not accessible by integration`. Ces résultats ne prouvent pas l'absence de protections. Les URL de liste workflows/tags sont refusées par le connecteur ; la lecture des références de tags indique un dépôt vide. Aucun paramètre de sécurité ni visibilité n'a été assoupli.

Le commit minimal d'amorçage est `26b7c773a0831c20e7f14bb86ef8c2697a19d523` (README seul), suivi des références de branches demandées. La PR documentaire cible `develop` ; aucune promotion produit ou mise en production n'en découle automatiquement.

## Inventaire des sources

| ID | Entrée | Autorité / limite |
|---|---|---|
| SRC-01 | Pièce jointe propriétaire `Texte collé.txt` | Mission documentaire/gouvernance immédiate ; pas un rapport de tests techniques |
| SRC-02 | Conversation ForgePanel/WCP360 visible | Demandes explicites et propositions ; les déclarations précédentes de l'assistant exigent corroboration |
| SRC-03 | `ForgePanel_Foundation_v0.7_source.zip` | 92 fichiers ; prototype CLI/setup, schéma, tests et rapports ; ni versionné ni publié sur GitHub |
| SRC-04 | `ForgePanel_Core_Foundation_v0.6_source.zip` | 14 fichiers plus répertoires ; prototype historique CLI/doctor/jeton fichier |
| SRC-05 | `ForgePanel_v0.7_README.md`, `ForgePanel_v0.7_Test_Report.md`, `.zip.sha256` | Déclarations/empreinte de livraison ; distinctes des tests relancés maintenant |

Les empreintes exactes figurent dans les [preuves sources](../../evidence/sources.json). L'empreinte fournie de v0.7 correspond à l'archive. L'extraction d'inspection refuse sorties de chemin et liens symboliques. Ce lot n'ajoute à Git aucune archive source, binaire généré, arborescence vendor ou secret opérationnel.

## Carte du contenu v0.7

| Chemin dans l'archive | Contenu observé |
|---|---|
| `cmd/forgepanel`, `internal/*` | CLI, doctor, planificateur non exécutable, pont console fixe, vérification de release et store historique |
| `apps/panel/src`, `config`, `templates` | Sources du setup Symfony, métier, dépôts SQL, routes et vues Twig |
| `apps/panel/migrations/001_setup.sql` | Trois tables bootstrap et contraintes d'unicité |
| `contracts`, `examples` | Schéma d'intention d'installation et exemple |
| `tests/fixtures`, `apps/panel/tests` | Fixtures OS, tests PHP mémoire et test PostgreSQL explicitement conditionné |
| `docs`, `tests/results` | Architecture, frontières, prochain jalon et résultats historiques |

Aucun `composer.lock`, démon agent complet, installateur de paquets, provisionnement web, RBAC complet ou moteur de plugins tiers n'est présent. Noms/empreintes permettent une correspondance exacte ultérieure ; ne pas reconstruire des sources manquantes à partir de leur description. Le prochain import vérifie les octets fournis et consigne le commit obtenu.
