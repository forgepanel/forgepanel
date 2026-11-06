<!-- forgepanel-doc id=FP-13-APP-EVIDENCE revision=1 status=specified -->
# App Center — preuves et frontières APPLY, tests d'intégration réels

[English](../../en/13-tests-quality/app-center-evidence-gates.md) · [QA](README.md) · [Contrat des preuves](../08-api-contracts/app-center-admission-evidence.md)

**PLANNED / NON EXÉCUTÉS.** Les 12 essais réels Core/Symfony/Go/VM ci-dessous ne sont pas accomplis par les exemples JSON ni par les tests Python hors ligne.

| ID | Contrôle | Résultat requis | État |
|---|---|---|---|
| TEST-EVID-FP-0001 | Authenticated host peer and target binding | Pair agent authentifié ; l'hôte cible ne peut pas être forgé par le navigateur | PLANNED |
| TEST-EVID-FP-0002 | Symfony actor/tenant/site RBAC | Refus d'acteur/organisation/site tiers sous vraie session Core | PLANNED |
| TEST-EVID-FP-0003 | Host observation freshness | Observation hôte expirée, future ou indisponible n'autorise ni plan ni APPLY | PLANNED |
| TEST-EVID-FP-0004 | Policy revision and TOCTOU | Modification concurrente de politique invalide aperçu périmé et APPLY revalide la révision | PLANNED |
| TEST-EVID-FP-0005 | Authorization revision and revocation | Droit acteur/site révoqué rend une intention précédente caduque avant APPLY | PLANNED |
| TEST-EVID-FP-0006 | Source signature and trust roots | Signature/éditeur falsifiés refusés ; identité du pair et rotation des clés testées | PLANNED |
| TEST-EVID-FP-0007 | Native One-Click autonomy | Installation native sans Hub, paiement ni Docker/Podman | PLANNED |
| TEST-EVID-FP-0008 | Container driver and measured budgets | Recette Docker refusée sur Podman non qualifié ; quotas CPU/RAM réels vérifiés | PLANNED |
| TEST-EVID-FP-0009 | Control-plane port isolation | FORGE 8447 et PANEL 8446 non attribuables, accès de secours maintenu | PLANNED |
| TEST-EVID-FP-0010 | Idempotency and fencing | Réessai clé/digest identique sans double effet ; ancien fencing refusé | PLANNED |
| TEST-EVID-FP-0011 | Recoverable partial failure | Crash après effet Linux/SQL partiel : état de reprise sincère et données préservées | PLANNED |
| TEST-EVID-FP-0012 | Hub cannot grant Core Linux authority | Licence, mise à jour ou diagnostic Hub ne confèrent aucun droit Go/Linux | PLANNED |

## Preuves nécessaires

Un PASS réel nécessite commit Core/agent/DB, OS/VM, identités authentifiées agent/acteur/tenant, horloge/snapshot de confiance et révisions, provenance d'artefact signée, logs de refus expurgés, véritables verrous et reprise vérifiée. BLOCKED/SKIP ne vaut pas PASS ; identité, temps, idempotence et récupération exigent des cas malveillants.

Cette matrice ne prouve aucune implémentation, audit de sécurité, permission hôte ni listener HTTPS fonctionnel. Q1–Q220 conservées ; Q221+ ouvertes.
