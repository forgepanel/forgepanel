<!-- forgepanel-doc id=FP-07 revision=2 status=documented -->
# Portails, identités et autorisations

[English](../../en/07-interfaces-roles/README.md) · [Index](../README.md)

## Un rôle applicatif n'est pas un privilège Linux

Les rôles cibles sont Super Administrator, administrateur serveur, revendeur, client d'hébergement et collaborateur limité. Seul `ROLE_SUPER_ADMIN` du compte initial existe dans le schéma SRC-03 ; ce n'est pas un RBAC complet. Linux `root`, le compte de service `forgepanel` et les comptes OS clients sont des sujets de sécurité distincts. Un rôle applicatif ne doit jamais ouvrir un shell root libre.

La décision d'autorisation cible combine permission, propriété client/ressource, délégation, état de la ressource et réauthentification sensible. Masquer un bouton ne protège pas l'opération. Contrôler séparément service, API et opération système ; refuser une autorité absente ou ambiguë. Ne pas déclarer les Voters Symfony configurés lorsque l'archive ne contient qu'un firewall de setup et des contrôles d'autorisation temporaire.

## Portails et sessions

Les accès directs cibles sont 8447 pour l'administration et 8446 pour les clients, puis des hôtes distincts configurables sur HTTPS 443. Le prototype accepte des ports non privilégiés distincts ; le portail client reste désactivé. Une même IP sur deux ports ne constitue pas une isolation des cookies. Hôtes distincts, contextes de session et autorisation serveur sont requis avant d'ouvrir les deux portails.

Le cookie de setup est configuré `__Host-FORGE_ADMIN`, Secure, HttpOnly, SameSite Strict, chemin `/`. Les tests HTTP réels restent à exécuter. `PUBLIC_ACCESS` des routes de setup ne supprime pas les contrôles jeton/autorisation de SetupService ; il ne crée pas non plus une session administrateur permanente.

## Tests exigés avant extension

Vérifier refus client-vers-admin, accès inter-comptes, périmètre revendeur, API directe sans UI, autorisations périmées/révoquées, rotation de session, déconnexion, CSRF, limites d'essais et rejeu des codes de secours. Auditer acteur et périmètre effectif sans identifiants secrets. Les guides revendeur/client restent futurs tant que ces parcours n'existent pas.

Le white-label Q5 ajoute une identité visuelle, des thèmes, des domaines HTTPS et des emails/templates par organisation ou revendeur. Les permissions de personnalisation ne donnent jamais accès aux fichiers/clients d'autrui, et l'héritage est défini dans le [Configuration Engine](../02-architecture/configuration-engine.md). Non disponible aujourd'hui.

Q58 C conserve les **comptes locaux** et propose un **SSO/OIDC facultatif**. Les identités, groupes et claims ne deviennent pas automatiquement des rôles administrateur. Liaison d'identité, validation des jetons, isolation par organisation et récupération locale exigent des tests. MFA administrateur **facultatif**. Voir [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

[Sécurité](../10-security/README.md) · [Core du setup](../03-core/README.md) · [Design system](../11-design-system/README.md)
