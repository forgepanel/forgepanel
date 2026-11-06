<!-- forgepanel-doc id=FP-00-RECON-Q171-220 revision=1 status=specified -->
# Q171–Q220 — contrôle de cohérence, autorités et handoffs

[English](../../en/00-project-control/reconciliation-q171-q220.md) · [Décisions approuvées](decisions-q171-q220.md) · [Tests planifiés](../13-tests-quality/mvp-gates-q171-q220.md)

**Statut : REVIEW / COHÉRENCE SOUS CONDITIONS, non validation de production.** Les 50 recommandations ont été **explicitement approuvées par le propriétaire le 6 novembre 2026**. Q1–Q170 restent applicables. Une plateforme largement administrable n'efface pas les validations spécialisées de sécurité, architecture, base de données, API/IPC et VM. Ce document est un **contrôle technique**, pas un audit indépendant externe.

## Constats réconciliés ou soumis à condition

| Référence | Résultat | Base conservée / action nécessaire |
|---|---|---|
| Q171/Q176 vs Q3/Q54/Q119/Q120 | **Cohérent, progressif** | Catalogue One-Click large à terme ; premier site PHP/HTTPS réel R4 avant recettes natives, puis conteneurs certifiés. Aucune promesse de vingt apps livrées ni date fixée. |
| Q172/Q216/Q218 vs Q47/Q66 et IPC typé | **Cohérent si borné** | API provisioning, connecteurs facturation et API publique utilisent des opérations versionnées ; aucun doublon incontrôlé, shell/root arbitraire ni permission choisie par client. Idempotence, scopes, audit et récupération exigés. |
| Q173/Q205 et Q174/Q206 | **Complémentaires** | Moteur antivirus multiscanner et WAF sont distincts. Q174 **C** : candidat Coraza + OWASP CRS, détection d'abord ; blocage, faux positifs et compatibilité OS/WebStack à qualifier, aucun déploiement présumé. |
| Q175 vs ADR-008 et clarification ultérieure ; Q5/Q55 | **Contradiction documentaire historique — delta ciblé nécessaire** | ADR-008 mentionne encore des hôtes système distincts. La directive récente impose **IP machine détectée/FQDN existant vérifié**, sans *domaine personnalisé des portails système*. Conserver **FORGE `/forge`:8447** et **PANEL `/panel`:8446**, sessions isolées ; marque unique par organisation et domaines des sites hébergés restent une fonction différente. Aucun sous-domaine `forge.`/`panel.` créé. Revue de la séparation des cookies par port nécessaire. |
| Q177/Q178/Q202 vs Q8/Q53/Q114 | **Cohérent avec revue** | Import local signé ≠ confiance automatique. Vérifier éditeur, licence, digest et **approbation humaine par version** ; aucun hook de catalogue libre. |
| Q180/Q220/Q190/Q214 vs Q55/Q66/tenants | **Cohérent avec plafonds** | Héritage et droits revendeur ne contournent jamais droits serveur/tenant, contraintes de sécurité, quotas physiques ou marque unique. Revendeurs plus tard, pas activés par ce vote. |
| Q181/Q182 vs Q83/Q86/Q91/Q101 | **Cohérent selon compatibilité** | SQL, PHP/extensions, versions épinglées/EOL suivent la compatibilité app/runtime certifiée. Pas de PHP/DB par défaut inventé. |
| Q183/Q184/Q185 vs Q47/Q65/Q75/Q90/Q156/Q166 | **Cohérent, reprise à prouver** | Mises à jour, sauvegardes fichiers+SQL et rétention ne garantissent ni rollback SQL ni restauration sans vrais essais. Aucun réglage automatique par défaut choisi. |
| Q188/Q189 vs Q94/Q104 | **Cohérent avec confidentialité** | Masquage staging, secrets séparés, mails/webhooks réels désactivés ; copies sensibles avec autorisation. Aucun secret client dans le Hub. |
| Q191–Q199 vs Q4/Q51/Q102/Q132 | **Cohérent sous certification** | Rootless favorisé mais pas supposé universel. Pilotes Docker/Podman, Compose, volumes, cgroups, réseau et exceptions après qualification par OS/VM. Un Compose Docker n'est pas automatiquement une recette Podman. |
| Q194 **C** vs D non retenu | **Option D non adoptée** | Manifestes/fournisseurs précisément qualifiés, pas d'exécuteur de Compose arbitraire ni d'éditeur graphique avancé de stacks approuvé. |
| Q200 **C** vs D non retenu | **Option D non adoptée** | Assistant export/import revu, avec sauvegarde et confirmation ; conversion native↔conteneur automatique générale **non approuvée**. |
| Q201–Q204/Q210 vs Q61/Q71/Q113/Q114 | **Cohérent sous contrôle local** | Catalogues signés, clés protégées, alertes et retraits par gravité, téléchargements SSRF-safe. Hub ne commande ni Linux ni effacement des données hébergées. |
| Q207/Q219 vs Q6/Q158/Q168 | **Cohérent seulement avec consentement** | Logs/métriques locaux administrables ; télémétrie Hub, diagnostics support et statistiques inter-organisations exigent consentement séparé, minimisation et anti-réidentification. |
| Q208 vs Q66/Q76/Q163 | **Cohérent** | Réauthentification/approbations et secours audité ; **MFA administrateur facultative**. Dérogations de performance non critiques seulement, jamais aux veto sécurité/récupération. |
| Q211–Q215 vs Q2/Q50 | **Cohérent si Core libre** | Deux catalogues, recherche commune en lecture seule, coûts tiers clairement distingués ; sponsor facultatif affiché distinctement, sans dégrader sécurité/compatibilité ni paywall natif. |
| Q217/Q218 vs permissions | **Cohérent si borné** | Webhooks signés/anti-rejeu et destinations approuvées ; API publique progressive avec opérations autorisées, pas de shell privilégié générique. |
| Q220 Configuration Center | **Objectif approuvé ; architecture ouverte** | Règles versionnées, héritage, simulation et récupération. L'interface ne modifie pas les invariants non désactivables. Pas de schéma/langage/rollout fixé. |

## Répartition des autorités

- **CORE / Produit + Modules :** registre canonique Q171–Q220 comme orientations ; exécution et données clients toujours locales au Core.
- **Security + Audit :** faux positifs WAF/scanner, droits SSH, privilèges conteneurs, SSRF, artefacts signés, télémétrie, TOCTOU et isolation clients. Les veto Q132 ne disparaissent pas.
- **API/IPC + Database :** API de provisioning/facturation, opérations Go typées, manifestes distincts, idempotence, réservations, migrations et récupération.
- **Design + QA + DevOps :** deux espaces App Center, prévisualisation, 50 cas de validation **PLANNED**, tests OS/VM et ordre d'intégration.
- **Hub éditeur privé :** métadonnées approuvées, éditeurs, versions, licences et prix affichés, promotions facultatives, événements/diagnostics limités et intégrations facturation. **Pas d'installation de sites, secrets clients, socket Docker, root Linux ou droit commercial obligatoire pour le natif gratuit.**

## Choix techniques qui restent ouverts

Liste et ordre des apps ; moteurs antivirus et flux de maintenance ; version du WAF et conditions de passage blocage ; profils rootless/Compose ; quotas, durées de rétention et fenêtres de mise à jour ; prestataires de paiement/identité et contrats API ; tarifs, licences et contrats sponsor ; clés de signature, fraîcheur cache, limites SSRF, proxies, sauvegardes, environnement de test et OS certifiés. Tout paramètre administrable doit garder une **contrainte de sécurité, un éditeur autorisé, un historique et une valeur par défaut uniquement après décision**.

## Preuves et étapes restantes

Cette mise à jour consigne les choix, périmètres et tests d'acceptation **PLANNED**. Une CI statique FR/EN ne prouve ni code opérationnel, ni protection WAF/antivirus, ni API, ni sécurité conteneurs. Les prérequis restent les vraies sources Foundation R1, Symfony/PostgreSQL R2, installateur R3, site PHP/HTTPS R4, puis ABI neutre R5 avant Hub R6. Les PR App Center parallèles doivent être réconciliées avant fusion. Aucun ancien arbitrage ni branche protégée n'est modifié silencieusement.
