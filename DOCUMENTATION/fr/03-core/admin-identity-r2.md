<!-- forgepanel-doc id=FP-03-ADMIN-IDENTITY-R2 revision=2 status=specified -->
# R2 — identité administrateur en lecture seule, candidat

[English](../../en/03-core/admin-identity-r2.md) · [QA](../13-tests-quality/r2-admin-readonly-qa.md) · [Contrats R2 existants](bootstrap-identity-r2.md)

**CODE PROPOSÉ / NON VALIDÉ POUR UN PANNEAU DE PRODUCTION.** Réutilisation des tables PostgreSQL Foundation v0.7.1 du compte initial, de son mot de passe Argon2id, des secrets TOTP chiffrés facultatifs, du compteur anti-rejeu, des codes de secours hachés et de l'audit. Aucune nouvelle table/DDL, opération Linux privilégiée, extension Hub, écoute réseau ou installation système n'est créée.

**PREUVES PARTIELLES VÉRIFIÉES — 07/11/2026 :** [PR #63](https://github.com/yyogas/forgepanel/pull/63), commit `97cfbf73100b237b8781e9c34bb0038ce7ccc1e4`, [CI push #42389509528](https://github.com/yyogas/forgepanel/actions/runs/42389509528) et [CI PR #42389514939](https://github.com/yyogas/forgepanel/actions/runs/42389514939) : **29 assertions PostgreSQL réelles** et **31 assertions de session HttpKernel Symfony + SQL** réussies. Sept contrôles statiques initiaux réussis. Seule la connexion en consultation est vérifiée ; ni R2 complet, ni authenticator Symfony Security/RBAC tenant, ni navigateur/TLS cookies, ni opérations serveur ne le sont.

## Connexion limitée

`AdminAuthentication` contrôle le mot de passe Argon2id en base ; un hash factice non sensible évite la reconnaissance immédiate d'un email inconnu. Les refus produisent le même message générique. Le singleton `fp_setup` doit être à `phase=REVIEWED` avec le compte initial correspondant et `ROLE_SUPER_ADMIN`. Cette phase signifie **plan examiné, jamais serveur installé** : seule `/admin` en consultation est accessible, sans pilotage de site, API ou root.

Lorsque l'utilisateur choisit facultativement la MFA, le TOTP exige un compteur strictement supérieur au dernier compteur commité sous verrou SQL ; les codes anciens sont refusés. Un code de secours hexadécimal de 24 caractères peut être consommé une seule fois dans la liste JSONB d'empreintes, sans exposer sa valeur. Lorsque la MFA est refusée, la connexion par mot de passe fonctionne et le secret d'enrôlement provisoire n'est pas conservé.

`AdminSessionController` expose GET/POST `/login`, GET `/admin`, POST `/logout`, avec CSRF sur login/logout, deux limiteurs Symfony candidats IP et empreinte IP+identifiant, rotation de l'identifiant de session, suppression du grant de setup et révocation à la déconnexion. La session contient uniquement l'ID administrateur, un horodatage et le HMAC des credentials/politique MFA ; chaque requête `/admin` revalide l'état SQL, l'ancienneté, le mot de passe/MFA. Une panne de base refuse l'accès. L'audit ne contient pas les secrets.

Le cookie `__Host-FORGE_ADMIN` reste Secure/HttpOnly/SameSite=Strict, chemin `/`, sans domaine ; la frontière HTTP refuse HTTP, mauvais Host, port ou Origin. Aucun proxy n'est implicitement fiable. Un refus CSRF ne modifie pas l'identité.

## Validations ouvertes

Il s'agit d'une **prévisualisation d'identité**, pas d'un authenticator Symfony Security complet ou d'un RBAC multi-tenant autorisant le provisioning. Avant toute opération réelle, imposer les revues Security/API/Database indépendantes, IPC signé et autorisé, qualification de l'installateur, authenticator et rôles complets, politique de session/révocation, tests CSRF et cookies en navigateur sous HTTPS, limiteur persistant multi-workers, reprise et restauration, et matrice R2 complète. Durées de session et quotas de tentative sont des valeurs candidates, pas des arbitrages définitifs. Le Hub et les modules futurs ne conditionnent jamais le login Core.
