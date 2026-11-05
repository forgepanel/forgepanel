<!-- forgepanel-doc id=FP-00-Q161-170 revision=1 status=specified -->
# Arbitrages Q161–Q170 — qualification, récupération et confidentialité

[English](../../en/00-project-control/decisions-q161-q170.md) · [Q151–Q160](decisions-q151-q160.md) · [Architecture](../02-architecture/evidence-and-recovery-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md)

**Choix confirmés le 5 novembre 2026. Q1–Q160 sont conservées et aucune question sans réponse n'est approuvée.** Statut SPECIFIED, non IMPLEMENTED ni VERIFIED.

| ID | Choix | Décision | Portée et sécurité |
|---|---|---|---|
| Q161 | C | Runners KVM éphémères isolés, images figées, quotas et nettoyage automatique | Q151 local d'abord, puis pilotes cloud. Vérifier capacités KVM, empreintes images/commits, ressources et nettoyage des secrets ; conserver les preuves signées hors runner. |
| Q162 | B | Stockage privé immuable des rapports signés avec historique, rétention et contrôle d'accès | Q152 rapports internes : vérifier signatures, provenance, snapshots, versions, historique et RBAC ; seconde réplication indépendante (option C) non adoptée. |
| Q163 | C | Exceptions de performance approuvées selon gravité, séparation des rôles, portée, expiration et révision | Q153/Q142 uniquement budgets de performance non critiques : approbateur différent du demandeur selon politique, révocation et audit. Veto sécurité, isolation et récupération Q132 non dérogeables. |
| Q164 | B | Contrôles DNS locaux et une sonde externe indépendante | Q154 : vérifier uniquement A/AAAA réellement publiés sur port 80/HTTP-01 et HTTPS ; la sonde externe doit être bornée, autorisée et protégée contre SSRF. Pas de réseau de sondes multiples (option C). |
| Q165 | C | Réparation non destructive bornée, checkpoints et validation humaine des opérations risquées | Q155 : actions système explicites allowlistées, tentatives et délais plafonnés, audit/état santé ; pas de shell root arbitraire ni de rollback destructif sans approbation. |
| Q166 | C | Restaurer chaque sauvegarde sur environnement isolé ; vérifications profondes périodiques et exercices de panne selon criticité | Q156 : sauvegarde récupérable seulement si périmètre complet restauré isolément PASS, clé de secours protégée accessible ; essais périodiques perte hôte/clé/panne sans détruire les vraies clés. |
| Q167 | C | SFTP par clé publique vérifiée, expiration, rotation, algorithmes autorisés, audit et contrôle sensible | Q157/Q146 : gestionnaire limité à ses sites ; possession de clé, quotas, confinement canonique, révocation, validation des opérations sensibles ; jamais de clé privée cliente ni shell. |
| Q168 | C | Consentements séparés, seuils par catégorie/cohorte, agrégation, expurgation et protection anti-réidentification | Q158/Q6 : pas de télémétrie forcée. Seuils configurables par donnée/cohorte, minimisation et protection contre recoupements ; santé locale et rapports manuels préservés sans Hub. |
| Q169 | C | Transferts premium simples automatisés sous règles de risque versionnées, seconde approbation et secours sécurisé | Q159/Q138/Q148 : identité, droits, org et challenge nonce vérifiés ; revue humaine et gel du transfert premium en cas de répétition, source perdue, incohérence ou compromission. Pas de moteur arbitraire par produit (Q159 D). |
| Q170 | B | Avis sous JSON Schema versionné, signé, validé, avec rendus FR/EN synchronisés et historique | Q160/Q150 : source canonique commune aux formes structurée et humaine, destinataires autorisés, notifications configurables et données sensibles protégées ; interopérabilité avancée option C non imposée. |

## Dépendances et restrictions

**R3** : Q161–Q163 = pilote KVM local, rapports signés privés immuables et exceptions de **performance non critique**. Les critères éliminatoires Q132 ne se négocient pas. **R4** : Q164–Q167 = sonde DNS externe indépendante + contrôle local des IP publiées, réparation non destructive bornée, restauration isolée de **chaque** sauvegarde avant statut récupérable, clés SFTP publiques sûres. **Après R4** : Q168 cohortes consenties sans télémétrie obligatoire. **Après API neutre R5** : Q169–Q170 concernent le Hub R6 (antifraude premium et avis JSON FR/EN), Core gratuit indépendant.

## Restent OPEN

Type d'hôte/runner KVM, capacités et quotas, stockage/signatures/rétention, seuils performance et approbations exactes, sélection et disponibilité de la sonde externe, plafonds de retry, calendrier des tests profonds/exercices, paramètres d'algorithmes SFTP, minimum statistique des cohortes, score risque de licence, JSON Schema final et canaux d'avis. **Aucune valeur ni date de livraison n'est inventée.**
