<!-- forgepanel-doc id=FP-08-PORTAL-ROUTING revision=2 status=specified -->
# Contrat candidat — découverte des accès et résolution FORGE / PANEL

[English](../../en/08-api-contracts/portal-route-boundary.md) · [Index API](README.md) · [Convention d'accès](../07-interfaces-roles/portal-access-routing.md)

**SPECIFIED, non implémenté.** Le propriétaire a corrigé la politique d'accès : **pas de domaine personnalisé à saisir**, détection automatique des IP de la machine et de son éventuel domaine existant vérifié. Les préfixes `/forge`, `/panel` et ports `8447`, `8446` restent fixés. Aucune URL ou opération réseau réelle n'est implémentée ici.

## Découverte IP et nom d'hôte, jamais depuis une requête cliente

1. **Host inventory** en lecture seule : interfaces réseau, routage, IPv4/IPv6 attribuées, adresses d'écoute ; conserver interface, famille IP, portée et statut. Ignorer loopback et les adresses non adaptées. Les adresses privées sont valables sur un réseau privé mais ne deviennent pas automatiquement publiques.
2. **FQDN existant** : demander au système le nom complet candidat (hostname et résolveur). Vérifier réellement A/AAAA et résolution vers les chemins autorisés/atteignables ; ni reverse DNS seul, ni `/etc/hosts`, ni `Host` reçu ne sont suffisants. En cas de NAT, vérifier une route effectivement atteignable avec une méthode explicitement autorisée ; sinon marquer `UNVERIFIED`.
3. **TLS** : le certificat doit couvrir l'adresse réellement utilisée (IP-SAN pour URL IP, nom DNS pour URL domaine). L'échec de validation n'est jamais contourné. Un listener déployé, un certificat et une sonde réseau vérifiée sont requis avant l'état `VERIFIED`.
4. **Affichage** : produire des liens uniquement pour les couples adresse/port/préfixe vérifiés. Si le FQDN n'existe pas, n'afficher **aucune URL domaine**, sans demander d'en saisir une. Les détails de certificat/NAT et fallback local sûr restent soumis à qualification.
5. **443** : ne pas générer automatiquement de virtual host, DNS ou redirection. Une infrastructure déjà opérationnelle en HTTPS 443 est une étude distincte et doit passer les mêmes contrôles, sans être une exigence de base.

## Matrice de résolution (origines illustratives)

| Requête | Décision de surface |
|---|---|
| `https://<IP-détectée>:8447/forge` | FORGE si écouteur, certificat et autorisation sont valides |
| `https://<IP-détectée>:8446/panel` | PANEL si écouteur, certificat et autorisation sont valides |
| `https://<IP-détectée>:8447/panel` | DENY |
| `https://<IP-détectée>:8446/forge` | DENY |
| `https://<FQDN-vérifié>:8447/forge` | FORGE si DNS, routage, TLS et droits sont vérifiés |
| `https://<FQDN-vérifié>:8446/panel` | PANEL si DNS, routage, TLS et droits sont vérifiés |
| `https://<FQDN-vérifié>:8447/panel` et `...:8446/forge` | DENY |
| FQDN absent, non résolu ou contredisant l'acheminement | Aucun lien domaine annoncé |
| IP détectée uniquement sur un LAN | URL LAN candidate, jamais prétendue publique |
| Host/proxy forgé ou domaine inconnu | DENY ; aucun droit ni redirection déduit de l'entrée non fiable |
| `https://<hôte>:443/forge` ou `/panel` | Non automatiquement pris en charge ; intégration distincte qualifiée |
| `/setup` historique | NON MIGRÉ ; revue nécessaire |

Pour IPv6, la syntaxe des URL utilise obligatoirement `[adresse]`. La même IP ou le même FQDN peut servir aux deux interfaces : ce sont les ports et préfixes, combinés aux autorisations, qui distinguent les surfaces. Les navigateurs partagent les cookies entre ports d'un même hôte : l'isolation de session n'est **jamais** déduite des ports.

## Frontières et erreurs de sécurité

- **Ingress** : listener + préfixe canonique + Host de confiance (si domaine) + TLS valide ; ne pas confondre un FQDN candidat découvert avec une autorisation de route. L'application ne fait pas confiance à un en-tête de surface défini par le client.
- **Symfony** : routes de deux espaces, cookies distincts host-only `Secure`, `HttpOnly`, `SameSite`, stockage/session/CSRF/rotation indépendants, RBAC côté services/API. MFA facultative, réauthentification et approbations des opérations sensibles selon Q66/Q76.
- **Go** : ne jamais déduire une permission Linux du seul préfixe, port ou rôle visuel. Réévaluer identité, portée et opération typée ; pas de `shell.exec` arbitraire.
- **Proxys** : seuls les proxys explicitement approuvés transmettent des `Forwarded`/`X-Forwarded-*` pris en compte. Les URL de callback sont calculées à partir des origines déjà vérifiées, jamais du Host brut.
- **UI/HUB** : bundles et thèmes isolés FORGE/PANEL ; Hub privé indépendant sans routes, secrets ou autorisations éditeur dans le Core public.
- **Installation** : aucun formulaire de personnalisation de nom d'hôte. Préserver le secours admin et ne jamais écraser les configurations réseau étrangères lors de la découverte.

## Critères et statut

Le [registre statique](../../../evidence/portal-access-registry-v1.json) et [ses tests candidats](../../../tests/documentation/test_portal_access_contract.py) contrôlent la cohérence, sans interroger les véritables interfaces ni certifier des URL. Les [22 tests HTTP/VM prévus](../13-tests-quality/portal-access-gates.md) doivent être exécutés après import source R1, application Symfony/PostgreSQL R2, et gateway TLS/installer R3. **Aucune adresse IP, domaine, certificat, listener ou route n'a été certifié par ce document.**
