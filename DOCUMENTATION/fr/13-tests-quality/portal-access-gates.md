<!-- forgepanel-doc id=FP-13-PORTAL-ACCESS revision=3 status=specified -->
# Tests FORGE / PANEL — IP et FQDN détectés

[English](../../en/13-tests-quality/portal-access-gates.md) · [QA](README.md) · [Accès](../07-interfaces-roles/portal-access-routing.md)

**État : PLANNED, non exécuté.** La détection IP/domaine et les routes Symfony ne sont pas opérationnelles. Un contrôle statique documentaire n'est ni un test TLS réel ni un test d'hébergement.

## Validation statique existante

Le [registre candidat](../../../evidence/portal-access-registry-v1.json), le [validateur offline](../../../scripts/validate_portal_access_registry.py) et les [tests unitaires documentaires](../../../tests/documentation/test_portal_access_contract.py) détectent notamment la réintroduction d'un domaine personnalisable ou d'un vhost 443 automatique. Ils ne réalisent **aucun** des scénarios HTTP/VM suivants.

## Matrice d'intégration et de VM à exécuter

Chaque test devra préciser commit SHA, OS/VM, IP attribuées, nom système, résultat DNS, certificats, routage/NAT, port, méthode, acteur, résultat, journaux expurgés et état PASS/FAIL/SKIP. Ne jamais traiter SKIP comme PASS.

| ID | Scénario | Résultat attendu |
|---|---|---|
| TEST-PORTAL-0001 | URL avec IP système détectée sur HTTPS 8447 + `/forge` et certificat IP valide. | Surface FORGE réservée aux admins authentifiés. |
| TEST-PORTAL-0002 | URL avec IP système détectée sur HTTPS 8446 + `/panel` et certificat IP valide. | Surface PANEL autorisée, sans privilège admin. |
| TEST-PORTAL-0003 | Un même FQDN existant et vérifié pour les deux ports. | `FQDN:8447/forge` et `FQDN:8446/panel`, sans exiger deux sous-domaines. |
| TEST-PORTAL-0004 | FQDN inconnu, Host falsifié, SNI/certificat erroné. | Refus sûr, aucune autre surface révélée. |
| TEST-PORTAL-0005 | Client PANEL invoquant `/forge` par URL directe ou API. | Refus en amont et dans les services/agent, aucun job privilégié. |
| TEST-PORTAL-0006 | Même IP avec session FORGE envoyée à l'autre port. | Aucune authentification croisée ; cookies isolés par nom/contexte serveur, pas par port. |
| TEST-PORTAL-0007 | Login, logout, CSRF, SameSite, rotation des deux sessions. | Isolés et contrôlés indépendamment. |
| TEST-PORTAL-0008 | `Forwarded` et `X-Forwarded-*` non fiables. | Aucune redirection, origine ou permission dérivée du proxy falsifié. |
| TEST-PORTAL-0009 | `//`, chemins encodés, traversée, variantes de casse et alias. | Canonicalisation fiable, aucun contournement d'autorisation. |
| TEST-PORTAL-0010 | Bootstrap historique `/setup` migré vers FORGE. | Jamais exposé dans PANEL, jeton unique et contrôle de setup. |
| TEST-PORTAL-0011 | Bundles et widgets FORGE/PANEL. | Aucun conflit CSS/JS, RBAC indépendant du menu. |
| TEST-PORTAL-0012 | Changement de listener, TLS ou pare-feu par admin. | Plan, validation, conservation du secours, audit et récupération ; pas de formulaire domaine personnalisé. |
| TEST-PORTAL-0013 | FQDN d'un site client ou collision de listener. | Aucun détournement de site ou du Panel. |
| TEST-PORTAL-0014 | Callbacks, emails, liens absolus et redirections login. | URL générées uniquement depuis origines auto-détectées/vérifiées, jamais Host brut. |
| TEST-PORTAL-0015 | Core sans Hub éditeur. | Aucune route/secrets Hub ; Core autonome. |
| TEST-PORTAL-0016 | MFA activée ou passée ; opération sensible. | MFA facultative, réauthentification/permission/audit obligatoires selon politique. |
| TEST-PORTAL-0017 | URL IP sans certificat IP-SAN valide. | N'afficher aucune URL HTTPS présentée comme fiable ; diagnostic et secours sûr. |
| TEST-PORTAL-0018 | Requête `/` sur domaine existant ou 443 non préparé. | Aucune redirection/vhost 443 créé implicitement. |
| TEST-PORTAL-0019 | Aucun FQDN configuré ou DNS valide sur serveur. | IP seule comme candidat ; aucune URL domaine ni champ de saisie de domaine. |
| TEST-PORTAL-0020 | Plusieurs interfaces : IP privée, IP externe, loopback et NAT. | Inventaire avec provenance ; pas de supposition d'IP publique ; états vérifiés/non vérifiés. |
| TEST-PORTAL-0021 | IPv6 uniquement ou IPv4/IPv6 mixtes, selon interfaces. | Utiliser uniquement les IP détectées et utilisables ; IPv6 encadrée par `[ ]` dans URL. |
| TEST-PORTAL-0022 | FQDN retourne un A/AAAA externe non expliqué par interface/routage/NAT vérifié. | Marquer `UNVERIFIED` et refuser la promesse de domaine accessible. |

## Portes de sortie

R1 : source authentique ; R2 : application Symfony et PostgreSQL réels ; R3 : passerelle HTTPS, TLS et sonde d'accès ; R4 : isolation et parcours client. Les tests ci-dessus doivent être exécutés sur environnements et commits identifiés et suivis d'une revue sécurité. Les contrôles Python/documents restent distincts.
