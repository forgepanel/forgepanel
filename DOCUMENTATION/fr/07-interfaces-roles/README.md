<!-- forgepanel-doc id=FP-07 revision=7 status=documented -->
# Portails, identités et autorisations

[English](../../en/07-interfaces-roles/README.md) · [Index](../README.md)

## Un rôle applicatif n'est pas un privilège Linux

Les rôles cibles sont Super Administrator, administrateur serveur, revendeur, client d'hébergement et collaborateur limité. Seul `ROLE_SUPER_ADMIN` du compte initial existe dans le schéma SRC-03 ; ce n'est pas un RBAC complet. Linux `root`, le compte de service `forgepanel` et les comptes OS clients sont des sujets de sécurité distincts. Un rôle applicatif ne doit jamais ouvrir un shell root libre.

La décision d'autorisation cible combine permission, propriété client/ressource, délégation, état de la ressource et réauthentification sensible. Masquer un bouton ne protège pas l'opération. Contrôler séparément service, API et opération système ; refuser une autorité absente ou ambiguë. Ne pas déclarer les Voters Symfony configurés lorsque l'archive ne contient qu'un firewall de setup et des contrôles d'autorisation temporaire.

## Portails et sessions

La convention de portails confirmée est **FORGE** `/forge` sur HTTPS **8447** pour les administrateurs et **PANEL** `/panel` sur HTTPS **8446** pour les clients ; les hôtes HTTPS 443 dédiés sont configurables (exemples `forge.ip-server.com` et `panel.up-server.com`). Les accès IP complets sont `https://<server-ip>:8447/forge` et `https://<server-ip>:8446/panel`, seulement avec TLS valide. Voir le [contrat d'accès et de sécurité détaillé](portal-access-routing.md) et les [18 scénarios QA planifiés](../13-tests-quality/portal-access-gates.md). Le prototype accepte des ports non privilégiés distincts ; le portail client reste désactivé. Une même IP sur deux ports ne constitue **pas** une isolation des cookies. Hôtes, cookies/sessions et autorisation serveur doivent être séparés avant ouverture des deux portails.

Le cookie de setup est configuré `__Host-FORGE_ADMIN`, Secure, HttpOnly, SameSite Strict, chemin `/`. Les tests HTTP réels restent à exécuter. `PUBLIC_ACCESS` des routes de setup ne supprime pas les contrôles jeton/autorisation de SetupService ; il ne crée pas non plus une session administrateur permanente.

## Approbations, modes visuels et sessions (Q66, Q70)

L'administration des opérations sensibles exige réauthentification, avec **approbation supplémentaire configurable** lorsque la politique le demande (Q66 C). Le MFA reste facultatif ; prévoir procédure de secours contrôlée pour l'administrateur unique sans supprimer les audits. L'éditeur visuel (Q70 D) autorise seulement widgets et routes validés, sans transformer la visibilité d'un menu en permission. [Design](../11-design-system/visual-editor.md) · [Décisions](../00-project-control/infrastructure-decisions.md).

## Rôle gestionnaire de site Q136 C

Sur un site qu'il possède ou administre légitimement, le **gestionnaire de site** pourra voir l'état et modifier **PHP, domaine, TLS et fichiers**, utiliser **SFTP** et demander **sauvegarde/restauration** dans les limites de son plan, des quotas et des permissions Q47. Le rôle ne peut ni modifier paquets/mises à jour OS, paramètres globaux et sécurité du panneau, ni accéder aux sites d'une autre organisation ou élever ses droits. Les actions sensibles (TLS/restore) sont prévisualisées, auditées et approuvées selon politique ; MFA administrateur demeure facultatif. [Q131–Q140](../00-project-control/decisions-q131-q140.md). **Le rôle n'est pas implémenté.**

## Q146 C — accès SFTP restreint

Le gestionnaire de site (Q136) dispose uniquement du SFTP de ses propres sites/ressources autorisés, sous **identité OS cantonnée, chemins et symlinks sécurisés, clés d'accès, quotas effectifs et journaux d'audit**. Par défaut, SFTP **ne confère aucun shell**. Expiration ou révocation du droit interdit toute nouvelle connexion mais ne supprime pas les fichiers du compte. Test requis : accès au site possédé, refus d'un autre tenant, chemin parent, symlink et quota ; aucune option ne donne un terminal root. [Décisions Q141–Q150](../00-project-control/decisions-q141-q150.md).

## Gestion des clés publiques SFTP par site (Q157 C)

Le gestionnaire autorisé peut **enregistrer/révoquer des clés publiques** pour ses sites, dans la politique du compte/plan, avec limites de répertoires, expiration, quotas et audit d'accès. Toute action sensible (ex. nouvelle clé puissante, changement d'identité) peut exiger réauthentification/approbation ciblée Q66/Q76 ; **aucun téléversement de clé privée, shell root ni accès aux autres sites**. L'expiration/révocation ne supprime pas les fichiers. La sécurité doit être appliquée par les comptes Unix/serveurs SFTP, pas uniquement dans l'interface. [Contrats](../02-architecture/qualification-and-security-contracts.md).

## Tests exigés avant extension

Vérifier refus client-vers-admin, accès inter-comptes, périmètre revendeur, API directe sans UI, autorisations périmées/révoquées, rotation de session, déconnexion, CSRF, limites d'essais et rejeu des codes de secours. Auditer acteur et périmètre effectif sans identifiants secrets. Les guides revendeur/client restent futurs tant que ces parcours n'existent pas.

Le white-label Q5 ajoute une identité visuelle, des thèmes, des domaines HTTPS et des emails/templates par organisation ou revendeur. Les permissions de personnalisation ne donnent jamais accès aux fichiers/clients d'autrui, et l'héritage est défini dans le [Configuration Engine](../02-architecture/configuration-engine.md). Non disponible aujourd'hui.

Q58 C conserve les **comptes locaux** et propose un **SSO/OIDC facultatif**. Les identités, groupes et claims ne deviennent pas automatiquement des rôles administrateur. Liaison d'identité, validation des jetons, isolation par organisation et récupération locale exigent des tests. MFA administrateur **facultatif**. Voir [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

[Sécurité](../10-security/README.md) · [Core du setup](../03-core/README.md) · [Design system](../11-design-system/README.md)
