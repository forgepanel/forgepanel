<!-- forgepanel-doc id=FP-07-PORTALS revision=3 status=specified -->
# Accès FORGE / PANEL — ports fixes, IP et domaine détectés

[English](../../en/07-interfaces-roles/portal-access-routing.md) · [Rôles](README.md) · [Tests](../13-tests-quality/portal-access-gates.md)

> **SPECIFIED / non implémenté.** Correction explicitement donnée par le propriétaire le 6 novembre 2026 : **aucun champ « domaine personnalisé »**. ForgePanel détecte automatiquement l'adresse IP de la machine et, s'il existe, son nom de domaine utilisable. Les chemins et les ports décidés restent inchangés. Le prototype SRC-03 ne fournit pas encore ces deux portails.

## Accès attendus, sans domaine à saisir

| Surface | Adresse IP de la machine (détectée) | Si le FQDN de la machine est détecté et vérifié | Préfixe et port |
|---|---|---|---|
| FORGE, administration serveur | `https://<IP-détectée>:8447/forge` | `https://<FQDN-vérifié>:8447/forge` | `/forge`, 8447 |
| PANEL, hébergement client | `https://<IP-détectée>:8446/panel` | `https://<FQDN-vérifié>:8446/panel` | `/panel`, 8446 |

Pour une IPv6, entourer l'adresse de crochets : `https://[2001:db8::10]:8447/forge` (adresse illustrative de documentation). **Un seul FQDN existant peut servir aux deux espaces : ce sont le port et le préfixe qui définissent leur surface.** Ne jamais supposer `forge.domaine`, `panel.domaine` ou un sous-domaine généré automatiquement.

Le port **443 n'est pas une fonction automatique de ces accès** : un reverse proxy ou un virtual host 443 existant pourra être étudié ultérieurement, uniquement après qualification explicite. L'installateur ne crée ni DNS, ni domaine, ni alias automatiquement pour les deux portails. Le comportement de redirection depuis `/` n'est pas arbitré.

## Découverte automatique et vérification, sans fausse promesse

1. Interroger en lecture seule les interfaces réseau et la table de routage du serveur pour inventorier les IPv4 et IPv6 attribuées. Écarter les adresses loopback, non adaptées et celles des interfaces qui ne desservent pas le listener ; une adresse privée peut être valable depuis le LAN, mais n'est pas présumée publique.
2. Identifier la ou les adresses réellement utilisables pour chacun des listeners 8447/8446. Le NAT, les proxys, les IP externes et les pare-feux peuvent empêcher de déduire l'adresse publique de l'interface locale. Ne pas inventer une IP publique ni communiquer avec un service externe sans politique validée.
3. Interroger le nom d'hôte/FQDN du système comme **candidat**, sans considérer `/etc/hosts`, un simple reverse DNS ou une valeur `Host` reçue comme preuve. Vérifier la résolution A/AAAA, les adresses réellement publiées et l'acheminement jusqu'au serveur (y compris NAT explicitement vérifié).
4. Contrôler certificats TLS, SNI si applicable, listener et accessibilité. Une URL IP HTTPS ne peut être annoncée comme **fonctionnelle et fiable** sans certificat valide couvrant cette IP. Ne jamais inviter à ignorer les avertissements TLS.
5. Présenter les résultats avec leur état `VERIFIED`, `UNVERIFIED` ou `UNAVAILABLE`, leur origine et la cause d'une vérification négative. Si aucun domaine n'est trouvé, ne présenter **aucune URL par domaine**. Garder une procédure d'accès de secours locale sécurisée et testable.

Le choix du fournisseur de certificat, la découverte de NAT et les adresses d'écoute effectives sont des détails techniques ouverts, **pas des valeurs fixées**.

## Exigences de routage et de sécurité

| ID | Exigence | Vérification attendue |
|---|---|---|
| PORTAL-FP-0001 | FORGE conserve le préfixe `/forge` et HTTPS **8447**. | Listener/admin autorisé, pas de privilège Linux root automatique. |
| PORTAL-FP-0002 | PANEL conserve le préfixe `/panel` et HTTPS **8446**. | Listener/client et RBAC avec isolation des clients. |
| PORTAL-FP-0003 | IP détectée par le système ; FQDN existant découvert et **vérifié**, jamais configuré librement. | Pas de champ « domaine personnalisable » ou de sous-domaine automatique. |
| PORTAL-FP-0004 | L'autorisation s'applique sur HTTP, API, services et agent Go. | Interdiction des opérations admin pour un compte PANEL. |
| PORTAL-FP-0005 | Sessions et cookies administrateur/client indépendants ; MFA reste facultative. | Connexion, CSRF, rotation et déconnexion séparées. |
| PORTAL-FP-0006 | Ports différents sur une même IP ne garantissent pas l'isolation des cookies. | Noms de cookies distincts, sessions séparées et gardes serveur. |
| PORTAL-FP-0007 | Bootstrap historique `/setup` réservé à FORGE après migration et revue. | Aucun chemin de setup accessible depuis PANEL. |
| PORTAL-FP-0008 | Refus des hôtes et en-têtes proxy non fiables. | Protection contre Host spoofing, `Forwarded` falsifié, open redirect. |
| PORTAL-FP-0009 | Bundles JS/CSS/Twig/UX et thèmes par portail. | Pas de conflit d'assets ou de contournement par widget. |
| PORTAL-FP-0010 | Toute modification de listener, DNS/TLS, pare-feu ou accès de secours suit Q47. | Plan, sauvegarde, contrôle de santé, audit et récupération. |
| PORTAL-FP-0011 | Le Hub privé n'est pas une dépendance ni une route du Core standard. | Aucun secret ou droit d'éditeur accessible depuis ces deux interfaces. |
| PORTAL-FP-0012 | Les URLs générées utilisent uniquement les accès découverts **et vérifiés**. | Aucune URL inventée et aucune origine issue d'un `Host` brut. |

## Implémentation cible et limitations

- **Symfony** : routes `/forge/**` et `/panel/**`, firewalls, sessions et contrôles d'accès propres. L'agent Go vérifie indépendamment les opérations Linux typées ; aucune API `shell.exec` générique.
- **Découverte** : inventaire IP/FQDN en lecture seule, statut et provenance ; aucun changement DNS automatique. Si la vérification échoue, conserver les informations de diagnostic, ne pas fabriquer un lien opérationnel.
- **Installateur** : détecter les accès, choisir les interfaces d'écoute uniquement après qualification technique, vérifier TLS et pare-feu ; **aucune saisie de domaine personnalisé**. Garder le chemin d'administration de secours pendant toute modification.
- **UI** : header/sidebar, identité et CSS isolés entre FORGE et PANEL ; les autorisations sont indépendantes du thème.
- **Migration** : la route historique `/setup` et le cookie `__Host-FORGE_ADMIN` du prototype sont à réexaminer, et non déclarés opérationnels sous `/forge`.

[Contrat API/ingress](../08-api-contracts/portal-route-boundary.md) · [Registre candidat](../../../evidence/portal-access-registry-v1.json) · [Tests QA à exécuter](../13-tests-quality/portal-access-gates.md).

**État :** les validations du registre JSON et de la documentation sont uniquement statiques ; aucune découverte IP, sonde DNS/TLS, connexion Symfony, VM ou installation réelle n'est ici vérifiée.
