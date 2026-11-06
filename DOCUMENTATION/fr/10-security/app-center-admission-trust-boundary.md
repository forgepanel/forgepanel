<!-- forgepanel-doc id=FP-10-APP-TRUST revision=1 status=specified -->
# App Center — provenance des preuves et frontières d'autorisation du préflight

[English](../../en/10-security/app-center-admission-trust-boundary.md) · [Sécurité](README.md) · [Contrat d'aperçu](../08-api-contracts/app-center-preview-contract.md)

**MODÈLE DE SÉCURITÉ DRAFT / NON VÉRIFIÉ.** App Center nécessite *trois origines de confiance indépendantes* : capacités du serveur, autorisation authentifiée du Core et intention non fiable de l'utilisateur. Ce document précise un garde-fou architectural, **pas un protocole d'agent fiable déployé, un Voter opérationnel, un anti-rejeu implémenté ou un audit de sécurité approuvé**.

## Correction issue de la revue du code candidat

Le précédent préflight synthétique plaçait la liste des sites et le droit de gérer les conteneurs dans un même fichier de **capacités du serveur**. L'inventaire Linux ne prouve ni l'identité, ni l'organisation, ni les droits de l'utilisateur. Le prototype candidat distingue maintenant :

| Source | Informations | Future origine de confiance | Ne jamais déduire de |
|---|---|---|---|
| Capacités hôte | Identifiant serveur, PHP, pilotes SQL/conteneurs qualifiés, CPU/RAM/PIDs libres, ports réservés et occupés | Service/agent d'inventaire local validé, authentifié et limité au serveur cible | Formulaire client, catalogue, facture Hub, simple claim JWT |
| Autorisation Core | Acteur connecté, tenant, propriété des sites, permission d'action sur conteneurs | Identité Symfony côté serveur, RBAC, contrôles d'organisation/ressource et politique effective | Sonde Linux, widget plugin, requête non fiable |
| Demande d'installation | Références hôte/tenant/site, variante choisie, ports TCP demandés | *Intention* soumise par le client et normalisée par Core, jamais une permission | Paramètres HTTP non authentifiés prétendant être une autorité |

Ces objets peuvent partager des identifiants **uniquement pour les recoupements**. L'égalité de deux chaînes ou la présence d'un site dans une liste fictive **ne constitue pas une authentification** et ne garantit pas des droits à jour. L'API ne doit jamais accepter un rapport complet de capacités ou un contexte d'autorisation fourni par l'utilisateur.

## Implémentation candidate hors ligne

La [fiche de capacités hôte](../../../evidence/app-center-fixtures/host-capabilities.synthetic.json) ne contient maintenant **aucun acteur, site de tenant ou privilège conteneur**. Une [fiche d'autorisation séparée](../../../evidence/app-center-fixtures/authorization.synthetic.json) contient acteur/tenant/hôte/site fictifs et l'état explicite `SYNTHETIC_UNVERIFIED`. La [demande synthétique](../../../evidence/app-center-fixtures/install-request.synthetic.json) représente l'intention et les références de l'utilisateur.

L'[aperçu hors ligne](../../../scripts/preview_app_center_install.py) rejette tout champ additionnel prétendant attribuer des droits, les structures de scope invalides et les états `VERIFIED` auto-attribués. Une discordance hôte ou tenant produit `HOST_SCOPE_MISMATCH` ou `TENANT_SCOPE_MISMATCH` ; un site absent du périmètre donne `SITE_OWNERSHIP_UNVERIFIED`. L'aperçu retourne toujours :

```json
{
  "input_trust": {
    "host_capabilities": "SYNTHETIC_UNVERIFIED",
    "authorization_context": "SYNTHETIC_UNVERIFIED",
    "client_request": "UNTRUSTED_CANDIDATE"
  },
  "tenant_authorization_verified": false,
  "runtime_capabilities_verified": false,
  "execution_allowed": false,
  "apply_available": false
}
```

Il s'agit d'un **extrait de sortie illustratif**, pas d'un résultat signé ou approuvé. `MATCHES_SYNTHETIC_FACTS_ONLY` ne permet jamais d'installer quoi que ce soit, même en l'absence de contradiction fictive. Aucun verrou, réservation, jeton, journal d'audit ou effet Linux n'est créé.

## Décisions et essais obligatoires avant toute application réelle

1. **Identité du serveur :** choisir un canal agent/IPC authentifié, un rapport de capacités typé, versionné et limité, une preuve de provenance, une fraîcheur bornée et un contrôle des ports réellement en écoute. Cela n'autorise **aucune API root générique**.
2. **Identité de l'acteur :** Symfony authentifie, vérifie organisation, propriété des sites, délégation, plan et quotas ; réauthentification pour les actions sensibles si la politique l'exige (MFA administrateur facultative). La requête ne peut pas choisir son rôle ni inventer ses permissions.
3. **Artefacts :** authentifier la provenance de l'éditeur et les digests de paquets/images ; une empreinte fictive ne prouve rien. Le One-Click natif gratuit ne demande aucun entitlement Hub.
4. **Prévisualisation versus application :** la prévisualisation est informative. Un futur APPLY **réévalue au moment de l'effet** l'acteur, les politiques, la révision du job, les ressources, le digest, les ports et quotas sous verrou/fencing. Protéger TOCTOU, confusion hôte/tenant et rejouements. Les véritables verrous et opérations Go typées relèvent de leurs autorités.
5. **Isolation des ressources :** PHP/SQL/fichiers natifs d'un côté ; images/volumes/réseaux/CPU/RAM/PIDs conteneurs de l'autre. Pas de basculement implicite entre moteurs. Réserver les ports de contrôle **8447 FORGE** et **8446 PANEL**, même si un formulaire les omet.
6. **Confidentialité :** audit limité aux identifiants acteur/hôte/site nécessaires, provenance et droits effectifs expurgés ; aucun mot de passe, secret ni jeton complet. Le Hub ne reçoit pas les fichiers, identifiants SQL ou données privées des volumes des clients.

## Preuves et dépendances

Les [39 tests synthétiques d'aperçu](../../../tests/documentation/test_app_center_preview.py) couvrent notamment champs falsifiés, discordances hôte/tenant, droits manquants et états non vérifiés. Ils restent des **tests hors ligne de structures fictives**, pas de véritables tests d'authentification, d'isolation Linux ou de réseau. Les [32 scénarios applicatifs/VM](../13-tests-quality/app-center-engine-gates.md) restent **PLANNED** et exigent des revues Security/QA avant publication.

**HANDOFF nécessaire :** Security → API/IPC → Database → QA/VM → Architecture Review → MASTER. TTL, signature des rapports, rôles/ACL, racine de confiance, pilotes et budgets de ressources **ne sont pas inventés**. Les prérequis R1 Foundation, R2 Symfony/PostgreSQL et R4 premier site PHP/HTTPS restent applicables.
