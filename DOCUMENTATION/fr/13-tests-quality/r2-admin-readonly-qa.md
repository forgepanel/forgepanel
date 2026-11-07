<!-- forgepanel-doc id=FP-13-R2-ADMIN-QA revision=1 status=specified -->
# R2 — candidat de tests SQL réels pour connexion administrateur et session Symfony

[English](../../en/13-tests-quality/r2-admin-readonly-qa.md) · [Contrat d'identité](../03-core/admin-identity-r2.md) · [Matrice R2 complète](r2-integration-gates.md)

**Statut : PLANIFIÉ jusqu'à observation des journaux GitHub Actions sur le commit exact.** La CI utilise PostgreSQL 16 jetable (`forgepanel_test`, consentement explicite, schémas temporaires et nettoyage), PHP 8.3, Composer verrouillé, le véritable HttpKernel Symfony et MockArraySessionStorage. Identifiants et secrets uniquement fictifs, jamais réutilisables. Aucune opération Linux, systemd ou privilégiée.

Scripts prévus :
- `apps/panel/tests/admin_identity_r2.php` : login sur SQL après `REVIEWED`, mot de passe correct/incorrect, identité inconnue, MFA facultative, protection de session après changement de mot de passe, refus de rejeu TOTP, code de secours unique, audit sans secrets ; base dédiée.
- `apps/panel/tests/admin_http_r2.php` : GET `/login` avec CSRF, `/admin` anonyme 401, CSRF invalide 403, échecs de connexion génériques, rotation de session, `/admin` en consultation uniquement, logout POST avec CSRF et refus de l'ancienne session. MockArraySessionStorage ne représente pas de vrai navigateur ou de passerelle HTTPS.
- `tests/r2/test_admin_readonly_contract.py` : règles statiques/documentaires, sans preuve d'exécution métier.

Restent à réaliser : authenticator Symfony Security et RBAC complets, périmètres locataires, contrôle cookie/TLS en navigateur, concurrence réelle de processus, limitation globale multi-nœuds, cycle de vie/récupération admin, époques de restauration, installation effective et tous les cas R2 complets. Les PR sources, MFA, PostgreSQL et Symfony sont des brouillons empilés ; **PASS ne signifie ni merge ni release ni Pre-Alpha prête**.
