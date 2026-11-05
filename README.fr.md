# ForgePanel

**The Modern Linux Server Control Panel**  
Modern • Secure • Modular • Scalable

[English](README.md) · [Documentation](DOCUMENTATION/README.md) · [État du projet](DOCUMENTATION/fr/00-project-control/status.md) · [Changelog](CHANGELOG/CHANGELOG.md)

## Contenu du dépôt

La fondation documentaire et de gouvernance de ForgePanel. Le dépôt était vide lors de l'examen du 2026-11-05. Les archives sources Foundation v0.6/v0.7 fournies dans la conversation ont été examinées séparément ; elles **ne sont pas importées comme code applicatif** par ce lot documentaire. Leurs noms ne désignent pas des releases GitHub.

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

Vérifier la documentation avec `python3 scripts/check_documentation.py`. Les tests applicatifs décrits pour les archives nécessitent leurs sources ; ils ne s'exécutent pas depuis ce dépôt documentaire seul.

Workflow : `features/*` → `develop` → `stable` → `main` → `production`. Un nom de branche ne prouve aucun déploiement. Le choix de licence appartient au propriétaire ; ce lot n'accorde aucune nouvelle licence logicielle.
