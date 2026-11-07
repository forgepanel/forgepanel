# ForgePanel

**The Modern Linux Server Control Panel**  
Modern • Secure • Modular • Scalable

[English](README.md) · [Documentation](DOCUMENTATION/README.md) · [État du projet](DOCUMENTATION/fr/00-project-control/status.md) · [Changelog](CHANGELOG/CHANGELOG.md)

## Contenu du dépôt

ForgePanel a commencé par une fondation documentaire et de gouvernance (dépôt initialement vide le 05/11/2026). **Sur la branche distincte de PR R1**, un candidat de 66 fichiers sources Foundation v0.7 est présent avec empreintes SHA-256 et tests Go/PHP hors ligne ; il n'est **pas encore fusionné, juridiquement validé, qualifié, publié ni déployé**. Les ZIP historiques ne sont pas des releases GitHub. [Import R1 et preuves](DOCUMENTATION/fr/12-development/foundation-v07-source-import.md).

**Ce dépôt ne contient pas encore d'installateur de production ni de panneau d'hébergement déployable.** Ne pas exécuter une URL d'installation inventée ni confondre un contrôle documentaire réussi avec une certification du produit.

## Direction produit

Un plan de contrôle Symfony/PHP modulaire avec Twig/Symfony UX, un agent système Go, PostgreSQL et des opérations Linux à privilèges minimaux. La conception multi-distribution cible Debian 12/13, Ubuntu 24.04/26.04 et AlmaLinux 9/10 ; Nginx, Apache, Caddy, PHP-FPM et FrankenPHP sont des composants web prévus, pas des installations certifiées.

## Points d'entrée

| Lecteur | Point d'entrée |
|---|---|
| Propriétaire | [Périmètre, décisions et priorités](DOCUMENTATION/fr/00-project-control/README.md) |
| Agent IA | [Consignes du dépôt](AGENTS.md) |
| Contributeur | [Guide de contribution](CONTRIBUTING.md) |
| Relecteur sécurité | [Politique de sécurité](SECURITY.md) |
| Prochaine implémentation | [Relais et blocages](DOCUMENTATION/fr/18-contributing/handover.md) |

Vérifier la documentation avec `python3 scripts/check_documentation.py`. Sur la branche d'import, lancer aussi `python3 scripts/check_foundation_import.py`, puis `bash scripts/check.sh` pour les contrôles Go/PHP isolés. Ils ne valident ni Symfony/PostgreSQL réels ni installateur Linux.

Workflow : `features/*` → `develop` → `stable` → `main` → `production`. Un nom de branche ne prouve aucun déploiement. Le choix de licence appartient au propriétaire ; ce lot n'accorde aucune nouvelle licence logicielle.

### Correctif de sources MFA facultative empilé (brouillon)

Le [patch Foundation v0.7.1 de MFA administrateur facultative](DOCUMENTATION/fr/12-development/foundation-v071-optional-mfa.md) est soumis à une revue distincte. Il ajoute un choix explicite de saut, une migration PostgreSQL et des tests hors ligne, mais n'est **ni fusionné ni validé en Symfony/PostgreSQL réels**. L'installation effective reste interdite.
