<!-- forgepanel-doc id=FP-13-R2-ADMIN-QA revision=2 status=specified -->
# R2 — candidat de tests SQL réels pour connexion administrateur et session Symfony

[English](../../en/13-tests-quality/r2-admin-readonly-qa.md) · [Contrat d'identité](../03-core/admin-identity-r2.md) · [Matrice R2 complète](r2-integration-gates.md)

**PREUVES PARTIELLES VÉRIFIÉES — 07/11/2026 :** [PR #63](https://github.com/yyogas/forgepanel/pull/63), commit `97cfbf73100b237b8781e9c34bb0038ce7ccc1e4`, [CI push #42389509528](https://github.com/yyogas/forgepanel/actions/runs/42389509528) et [CI PR #42389514939](https://github.com/yyogas/forgepanel/actions/runs/42389514939) : **29 assertions PostgreSQL réelles** et **31 assertions de session HttpKernel Symfony + SQL** réussies. Sept contrôles statiques initiaux réussis. Seule la connexion en consultation est vérifiée ; ni R2 complet, ni authenticator Symfony Security/RBAC tenant, ni navigateur/TLS cookies, ni opérations serveur ne le sont. La CI utilise PostgreSQL 16 jetable (`forgepanel_test`, consentement explicite, schémas temporaires et nettoyage), PHP 8.3, Composer verrouillé, le véritable HttpKernel Symfony et MockArraySessionStorage. Identifiants et secrets uniquement fictifs, jamais réutilisables. Aucune opération Linux, systemd ou privilégiée.

Scripts prévus :
- `apps/panel/tests/admin_identity_r2.php` : login sur SQL après `REVIEWED`, mot de passe correct/incorrect, identité inconnue, MFA facultative, protection de session après changement de mot de passe, refus de rejeu TOTP, code de secours unique, audit sans secrets ; base dédiée.
- `apps/panel/tests/admin_http_r2.php` : GET `/login` avec CSRF, `/admin` anonyme 401, CSRF invalide 403, échecs de connexion génériques, rotation de session, `/admin` en consultation uniquement, logout POST avec CSRF et refus de l'ancienne session. MockArraySessionStorage ne représente pas de vrai navigateur ou de passerelle HTTPS.
- `tests/r2/test_admin_readonly_contract.py` : règles statiques/documentaires, sans preuve d'exécution métier.

Restent à réaliser : authenticator Symfony Security et RBAC complets, périmètres locataires, contrôle cookie/TLS en navigateur, concurrence réelle de processus, limitation globale multi-nœuds, cycle de vie/récupération admin, époques de restauration, installation effective et tous les cas R2 complets. Les PR sources, MFA, PostgreSQL et Symfony sont des brouillons empilés ; **PASS ne signifie ni merge ni release ni Pre-Alpha prête**.
