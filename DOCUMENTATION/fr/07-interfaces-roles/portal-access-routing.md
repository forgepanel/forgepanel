<!-- forgepanel-doc id=FP-07-PORTALS revision=2 status=specified -->
# Contrat d'accès FORGE / PANEL — chemins, domaines et ports

[English](../../en/07-interfaces-roles/portal-access-routing.md) · [Portails et rôles](README.md) · [Tests](../13-tests-quality/portal-access-gates.md)

> **SPECIFIED — pas implémenté ni certifié.** Convention produit réaffirmée par le propriétaire le 6 novembre 2026. Le prototype SRC-03 ne livre pas deux portails fonctionnels. Les noms de domaine ci-dessous sont des exemples configurables, non des domaines déployés.

## Contrat d'accès retenu

| Surface | Accès direct HTTPS par IP | Hôte HTTPS configuré sur 443 | Préfixe canonique | Audience |
|---|---|---|---|---|
| **FORGE** (administration du serveur) | `https://<server-ip>:8447/forge` | `https://forge.ip-server.com/forge` | `/forge` | Super administrateur / administrateurs serveur autorisés |
| **PANEL** (hébergement client) | `https://<server-ip>:8446/panel` | `https://panel.up-server.com/panel` | `/panel` | Clients, gestionnaires de sites, revendeurs et collaborateurs autorisés |

Les hôtes d'exemple sont remplaçables par l'administrateur dans les limites d'une politique d'hôtes autorisés. L'adresse `<server-ip>` est illustrative : la disponibilité d'IPv4/IPv6 et d'un certificat valide avec cette IP doit être vérifiée. Aucun accès HTTPS sûr ne doit nécessiter de désactiver la validation TLS. Les deux sites sur 443 doivent être routés par SNI/Host **et** par politique d'hôte explicite. Les ports directs demeurent séparés des listeners des sites clients.

**Évolution proposée, à qualifier :** une requête `/` sur l'hôte FORGE configuré pourrait rediriger vers `/forge`, et `/` sur l'hôte PANEL vers `/panel`, uniquement après installation et validation du routage. Ne pas créer de redirection inter-portail ni forcer la propriété du chemin `/` sur des hôtes non dédiés.

Le [contrat API/ingress détaillé](../08-api-contracts/portal-route-boundary.md) et le [registre candidat JSON](../../../evidence/portal-access-registry-v1.json) précisent les refus par combinaison hôte/port/préfixe. Les hôtes illustrent une alternative d'accès dédié ; la réponse exacte de leur chemin racine `/` reste à qualifier.

## Exigences de routage et de sécurité

| ID | Exigence | Vérification attendue |
|---|---|---|
| PORTAL-FP-0001 | `/forge` et port 8447 appartiennent à la surface Admin FORGE. | Route et service HTTPS admin vérifiés, pas de privilège root applicatif implicite. |
| PORTAL-FP-0002 | `/panel` et port 8446 appartiennent à la surface User PANEL. | Routes utilisateurs sous autorisation serveur, clients isolés. |
| PORTAL-FP-0003 | Les deux noms d'hôte sur HTTPS 443 sont configurables et validés séparément. | SNI, `Host`, reverse proxy et certificats contrôlés ; hôtes non autorisés rejetés. |
| PORTAL-FP-0004 | Le contrôle d'accès opère sur HTTP **et** API/services/agent Go. | Un client ne peut pas atteindre les opérations admin via URL directe, API, alias, méthode ou job. |
| PORTAL-FP-0005 | Sessions et cookies admin/user sont distincts, hôte + serveur ; MFA reste facultative. | Cookies host-only Secure/HttpOnly, sessions stockées séparément, rotation/CSRF et logout indépendant. |
| PORTAL-FP-0006 | L'accès par IP:port ne constitue pas une frontière de cookies. | Noms de cookies distincts et contrôle serveur : un navigateur partage des cookies entre ports d'un même hôte. |
| PORTAL-FP-0007 | Les routes d'initialisation/reprise d'administration sont limitées au bootstrap FORGE. | Le prototype `/setup` est migré/encapsulé explicitement après import et tests ; aucune exposition PANEL. |
| PORTAL-FP-0008 | Les en-têtes `Forwarded`/`X-Forwarded-*` sont traités seulement depuis des proxys approuvés. | Aucune élévation via Host spoofing, préfixe injecté, schéma falsifié, redirection ouverte. |
| PORTAL-FP-0009 | Les assets Twig/UX/Tailwind et styles des deux espaces sont isolés. | Bundles et racines CSS distincts, composants partagés seulement via contrats, sans fuite de thème ni de droits. |
| PORTAL-FP-0010 | Toute modification d'hôte, port, TLS ou pare-feu est une opération sensible Q47. | Préflight, prévisualisation, accès admin de secours, validation, audit et récupération en cas de panne. |
| PORTAL-FP-0011 | Le Hub éditeur reste une extension/service privé indépendant. | Aucune route de publisher ou secret Hub monté dans un Core standard. |
| PORTAL-FP-0012 | Les liens, emails et URLs de callback utilisent l'origine autorisée et le préfixe de leur surface. | Jamais de génération d'URL depuis un Host non vérifié ; aucune fuite des jetons inter-portails. |

## Proposition de découpage d'implémentation

- **Symfony** : espaces de routes distincts (`/forge/**`, `/panel/**`), firewalls, sessions, politiques RBAC et services d'autorisation indépendants. Le Core contrôle chaque opération ; il ne délègue pas l'autorisation à un affichage de menu.
- **Passerelle HTTPS** : listeners directs 8447/8446 ; hôtes FORGE/PANEL configurables sur 443 après DNS/TLS valide. Refus des combinaisons host/port/préfixe non autorisées, même via reverse proxy. Garder le plan de contrôle accessible indépendamment des configurations WebStack des hébergements.
- **Frontend** : noms techniques séparés et versionnés pour les bundles FORGE et PANEL, par exemple `forge-admin` et `forge-user` (candidats, pas des assets existants). Tokens de marque partagés sous contrôle, racines CSS distinctes, entêtes/sidebar personnalisables par portail, et widgets soumis au RBAC.
- **Installateur** : wizard proposant les hôtes et vérifiant conflit IP:port, règles pare-feu, certificat, SNI et accès de secours ; ne pas modifier un listener tiers sans preuve de propriété. Reprise idempotente après échec.
- **Migration prototype** : les chemins `/setup` et le cookie de bootstrap `__Host-FORGE_ADMIN` existants dans SRC-03 nécessitent une revue de compatibilité. Ne pas prétendre qu'ils sont déjà routés sous `/forge`. Les noms définitifs des cookies permanents et la politique des alias/redirections restent à qualifier.

## Critères de sortie et statuts

Les scénarios vérifiables sont dans la [matrice QA](../13-tests-quality/portal-access-gates.md) et doivent être exécutés sur un vrai Symfony + PostgreSQL et sur une VM avec HTTPS. Les tests statiques/documentaires ne prouvent ni séparation de sessions ni fonctionnement des ports. **R1/R2/R3/R4 restent soumis aux gates existants ; aucune route active n'est introduite par cette fiche.**

Documents connexes : [Design system](../11-design-system/README.md) · [Installation](../14-devops-releases/README.md) · [Contrats API](../08-api-contracts/README.md) · [Sécurité](../10-security/README.md).
