<!-- forgepanel-doc id=FP-13-PORTAL-ACCESS revision=1 status=specified -->
# Matrice de tests — accès FORGE / PANEL

[English](../../en/13-tests-quality/portal-access-gates.md) · [QA](README.md) · [Contrat des portails](../07-interfaces-roles/portal-access-routing.md)

**État : PLANNED.** Ces cas n'ont pas été exécutés. La documentation actuelle ne fournit ni serveur Symfony intégré, ni gateway HTTPS certifiée, ni Panel client opérationnel. Les identifiants sont des objectifs vérifiables, pas des résultats `PASS`.

## Environnement et preuve obligatoire

Pour chaque essai : commit SHA et version Core, distribution/VM qualifiées, configuration de listeners, certificats, origines DNS, profil d'authentification, commande/navigation, résultat réel, logs expurgés et identifiant de corrélation. Exécuter d'abord sous tests HTTP/SQL/HTTPS intégrés, puis en VM complète ; ne pas confondre test unitaire et exposition Internet.

| ID | Scénario | Résultat attendu |
|---|---|---|
| TEST-PORTAL-0001 | `https://<server-ip>:8447/forge` avec TLS IP valide. | Surface FORGE disponible pour administrateur authentifié, sinon login/accès refusé sans contenu privilégié. |
| TEST-PORTAL-0002 | `https://<server-ip>:8446/panel` avec TLS IP valide. | Surface PANEL accessible aux rôles clients autorisés seulement ; pas de privilèges FORGE. |
| TEST-PORTAL-0003 | Hôtes distincts sur 443 avec SNI/certificats valides. | Domaine FORGE → `/forge` ; domaine PANEL → `/panel` ; pas d'interversion. |
| TEST-PORTAL-0004 | Domaine inconnu, Host falsifié, absence de SNI ou mauvais certificat. | Refus sûr, aucune réponse d'un portail étranger ni fuite de données. |
| TEST-PORTAL-0005 | Client connecté appelle `/forge` directement, avec API ou requête modifiée. | Refus sur l'ensemble des couches, sans job privilégié ni effet système. |
| TEST-PORTAL-0006 | Session FORGE sur IP identique mais port PANEL (et inversement). | Pas d'authentification croisée, malgré le partage des cookies entre ports d'un même hôte. |
| TEST-PORTAL-0007 | Cookies/sessions Admin et User, logout, rotation, CSRF, SameSite. | Portées strictement distinctes et aucune réutilisation du jeton de session. |
| TEST-PORTAL-0008 | Requêtes avec `Forwarded`, `X-Forwarded-Host/Proto/Prefix` forgés depuis une source non fiable. | Valeurs ignorées/refusées, URL et redirections non contrôlées par l'attaquant. |
| TEST-PORTAL-0009 | Encodages de chemins, `//`, `..\`, casse et alias de routes. | Normalisation sûre et mêmes permissions sur tous les chemins résolus ; aucun contournement. |
| TEST-PORTAL-0010 | Setup initial `/setup` et futur parcours `/forge` après import. | Accès bootstrap FORGE uniquement, jeton à usage unique ; aucune ouverture de setup depuis PANEL. |
| TEST-PORTAL-0011 | Assets/menus/widgets FORGE et PANEL sur desktop/mobile. | Bundles/styles isolés ; masquer un élément ne permet pas d'appeler une API non autorisée. |
| TEST-PORTAL-0012 | Modification admin de DNS, domaine Panel, TLS, port ou pare-feu. | Plan, autorisation, tests, maintien d'un accès de secours, audit et récupération si échec. |
| TEST-PORTAL-0013 | Requête sur un hôte de site client/route frontend ambiguë. | Site client et Panel ne prennent pas la place l'un de l'autre, pas de collision de listener. |
| TEST-PORTAL-0014 | Callbacks, liens d'email, liens absolus, redirections de login. | Origine configurée et autorisée, préfixe correct ; aucun `Host` arbitraire ni token inter-portail. |
| TEST-PORTAL-0015 | Serveur Core standard sans Hub ni plugin éditeur. | Aucune route publisher privée ni secret Hub ; administration et hébergement indépendants du Hub. |
| TEST-PORTAL-0016 | MFA facultative activée/non activée, réauthentification sensible. | Les deux parcours restent valides selon Q66/Q76 ; contrôle d'accès et audit restent obligatoires. |
| TEST-PORTAL-0017 | Indisponibilité DNS/certificat pour accès IP et accès de secours. | Signalement explicite, aucune consigne de contournement TLS ; alternative locale sûre qualifiée. |
| TEST-PORTAL-0018 | Redirection de `/` sur chaque domaine dédié, si approuvée. | Redirection uniquement vers le préfixe du même portail ; jamais vers un hôte externe/voisin. |

## Critères de validation

La documentation bilingue, les contrats d'API, le modèle d'identité, la configuration des proxies et le Design System doivent utiliser la même convention. Tout changement de port/hôte ou de route critique nécessite un test de non-régression. Une maquette, un contrôle statique ou une PR verte ne suffisent pas à certifier la route ; seuls les essais réels sur la révision évaluée permettent `VERIFIED`.

Dépendances : [R2 identité](../03-core/bootstrap-identity-r2.md) · [R3 installateur](../14-devops-releases/installer-lifecycle-r3.md) · [Sécurité](../10-security/README.md).
