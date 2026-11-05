<!-- forgepanel-doc id=FP-00-COVERAGE revision=1 status=documented -->
# Matrice de couverture documentaire

[English](../../en/00-project-control/coverage.md) · [Pilotage](README.md)

Chaque catégorie possède un index français/anglais substantiel et une navigation réciproque. Il s'agit de couverture documentaire, pas de spécifications d'implémentation toutes achevées. `Documenté` signifie périmètre/preuves/acceptation décrits ; `Partiel` précise les détails manquants ; `Absent` désigne le logiciel manquant, pas des documents vides.

| Catégorie | Couverture livrée | Spécification ou implémentation restante |
|---|---|---|
| 00 Pilotage | Gouvernance, états, décisions, roadmap | Arbitrages licence/publication ouverts |
| 01 Produit | Profils, parcours, acceptation | Stories détaillées hébergement/revendeur partielles |
| 02 Architecture | Frontières, dépendances, profils | Pilotes OS/paquets/runtime concrets absents |
| 03 Core | Machine d'états réelle du setup, noyau cible | Agent durable/jobs/registre de modules absents |
| 04 Modules | Catalogue et fiches composants | Implémentations d'hébergement natives absentes |
| 05 Plugins | Confiance, cycle de vie, acceptation | Manifeste versionné/isolation partiels ; moteur absent |
| 06 Apps/recettes | Fiche recette et récupération | Schéma/catalogue/exécuteur absents |
| 07 Interfaces/rôles | Portails, rôles, distinction des privilèges | RBAC contextualisé et login permanent absents |
| 08 API/contrats | Schéma/routes/CLI réels et enveloppe cible | API publique/protocole agent non finalisés |
| 09 Base | Schéma réel à trois tables et règles de migration | Tests SQL réels en attente ; modèle hébergement absent |
| 10 Sécurité | Frontières, menaces, critères, signalement | Canal privé et audit indépendant absents |
| 11 Design system | Marque, états, accessibilité, stratégie i18n | Tokens visuels validés et infrastructure de traduction absents |
| 12 Développement | Conventions, commandes applicables, import | Environnement de dépendances verrouillé en attente |
| 13 Tests/qualité | Niveaux de preuve et définition de terminé | Campagnes intégration/navigateur/VM absentes |
| 14 DevOps/releases | Workflow, exception d'amorçage, critères | Paquets, installateur et cycle de signature absents |
| 15 Exploitation | Limites CLI et procédure d'incident cible | Réparation/sauvegarde/restauration fonctionnelles absentes |
| 16 Performance | Protocole de mesure et contraintes de sécurité | Benchmarks et seuils de capacité absents |
| 17 Guides | Limites actuelles et parcours visés | Guides client/revendeur vérifiés après implémentation |
| 18 Contribution | Accueil humain/IA, PR et relais | Visibilité des exigences de revue/protection non résolue |
| 19 Audit/risques | Provenance dépôt/archives et contradictions | Aucun audit exhaustif code/sécurité/production |

Actualiser cette matrice lorsqu'une lacune change d'état. Toute fonction `VERIFIED` exige une preuve nommée sur une entrée identifiée ; toute publication exige une trace réelle release/tag/artefact. Les métadonnées de traduction sont contrôlées automatiquement ; le sens est relu séparément.
