<!-- forgepanel-doc id=FP-08-PORTAL-ROUTING revision=1 status=specified -->
# Contrat candidat — résolution de surface FORGE / PANEL

[English](../../en/08-api-contracts/portal-route-boundary.md) · [Index API](README.md) · [Convention d'accès](../07-interfaces-roles/portal-access-routing.md)

**Statut : SPECIFIED / PAS IMPLÉMENTÉ.** Cette fiche complète `PORTAL-FP-0001..0012` ; elle ne crée ni API publique, ni route Symfony, ni listener HTTPS, ni validation de sécurité opérationnelle. L'import Foundation v0.7 et l'intégration R2 Symfony/PostgreSQL restent des prérequis.

## Décision de surface, avant authentification

Le frontal de confiance détermine une surface par la **conjonction** de l'écouteur local, de l'hôte HTTPS autorisé, du certificat applicable et du préfixe de chemin canonique. La surface reste un contexte de sécurité, jamais un rôle de permission ou un jeton transmis par le navigateur. Les hôtes `forge.ip-server.com` et `panel.up-server.com` sont des exemples, pas des paramètres de production fixés.

| Origine et chemin (exemples) | Résolution cible | Condition |
|---|---|---|
| `https://<IP>:8447/forge` | FORGE | TLS valide pour IP, listener admin, utilisateur admin autorisé |
| `https://<IP>:8446/panel` | PANEL | TLS valide pour IP, listener client, utilisateur autorisé |
| `https://<IP>:8447/panel` | DENY | Pas de repli vers PANEL sur le listener admin |
| `https://<IP>:8446/forge` | DENY | Pas de repli vers FORGE sur le listener client |
| `https://<forge-host-configuré>:443/forge` | FORGE | Hôte exact, SNI/certificat, proxy fiable, rôles admin |
| `https://<panel-host-configuré>:443/panel` | PANEL | Hôte exact, SNI/certificat, proxy fiable, rôles clients |
| `https://<forge-host-configuré>:443/panel` | DENY | Aucun routage inter-portail |
| `https://<panel-host-configuré>:443/forge` | DENY | Aucun routage inter-portail |
| `https://<hôte-inconnu>:443/forge` | DENY | Liste d'hôtes autorisés, pas de vhost par défaut permissif |
| `http://<hôte>:80/forge` | DENY/redirect sûr uniquement après politique | Jamais de session admin ou secret sur HTTP non chiffré |
| `/setup` historique SRC-03 | NON MIGRÉ | Revue spéciale bootstrap avant toute nouvelle exposition |

**Remarque :** l'absence de certificat IP valide n'autorise pas une exception de validation TLS. Une option d'accès de secours local sûr doit être qualifiée avant d'ouvrir le service. Redirection facultative de `/` vers `/forge` ou `/panel` : **proposition non arbitrée**.

## Interfaces Symfony et responsabilité

- **Routes** : espaces logiques `FORGE` et `PANEL` ; les routeurs ne font pas confiance à une valeur de surface fournie par le client. Les chemins encodés, alias, chemins doubles ou normalisés ne peuvent pas contourner une garde.
- **Sessions** : contextes de connexion et noms de cookies distincts, gestion serveur indépendante, `Secure`, `HttpOnly`, `SameSite`, CSRF et rotation. Un cookie lié à la même IP peut être transmis à **8446 et 8447** ; le port n'isole pas les cookies. Le cookie provisoire `__Host-FORGE_ADMIN` du prototype n'est pas la décision définitive pour les sessions durables.
- **Authentification** : comptes locaux et éventuel SSO selon Q58 ; MFA administrateur **facultative**. Réauthentification/approbation Q66/Q76 pour les opérations sensibles. Un utilisateur autorisé sur PANEL n'acquiert aucun rôle FORGE par une manipulation d'URL.
- **Autorisation** : décisions du Core sur rôle + organisation + propriété de ressource + délégation + état + politique ; vérification nouvelle au service/API et à l'agent Go avant tout effet Linux. Aucune opération générique `shell.exec` ni injection d'une commande fournie par client.
- **En-têtes de proxy** : configurer précisément les adresses de proxys de confiance ; rejeter/ignorer les `Forwarded` et `X-Forwarded-*` étrangers. Les URLs absolues/callbacks utilisent l'origine configurée, pas `Host` brut.
- **UI** : entrées de compilation, racines de styles et thèmes séparés pour FORGE et PANEL ; composants réutilisables seulement sous contrats validés. Un bundle JavaScript ou un widget ne définit pas un privilège. Hub privé sur son service séparé, sans routes publiques éditeur du Core.

## Dépendances d'implémentation

1. **R1** : obtenir et importer la véritable archive Foundation v0.7 avec empreinte et provenance, sans recréer les sources manquantes.
2. **R2** : faire fonctionner Symfony et PostgreSQL réels, avec routes, firewall, sessions, comptes permanents et bootstrap/MFA facultative.
3. **R3** : installateur et gateway HTTPS qualifiés ; configurer port, IP, hôtes, DNS/TLS et pare-feu via plan `validate → apply → health → recover`, en préservant un accès secours.
4. **R4** : tests d'isolement sur les sites hébergés et leurs listeners, avant publication d'un portail client.
5. **R5/R6** : ABI externe neutre puis Hub éditeur privé, sans dépendance de l'accès FORGE/PANEL.

## Registre et tests statiques

Le [registre candidat JSON](../../../evidence/portal-access-registry-v1.json) est une représentation **non exécutable** des chemins/ports/invariants, vérifiée par [un validateur offline](../../../scripts/validate_portal_access_registry.py) et [des tests unitaires de contrat](../../../tests/documentation/test_portal_access_contract.py). Ces outils détectent des contradictions de documentation, **pas** les failles d'un serveur ni le fonctionnement effectif de Symfony. Les [18 tests HTTP/VM](../13-tests-quality/portal-access-gates.md) restent `PLANNED`.

Contrôle des choix ouverts : domaines réels, certificats IP, politique de proxy de confiance, noms définitifs des cookies et redirection de `/` — **aucune valeur non arbitrée n'est inventée**.
