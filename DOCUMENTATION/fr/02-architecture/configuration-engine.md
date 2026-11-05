<!-- forgepanel-doc id=FP-02-CONFIG revision=5 status=specified -->
# Configuration Engine — spécification des réglages administrables

[English](../../en/02-architecture/configuration-engine.md) · [Architecture](README.md) · [Politique produit](../00-project-control/product-policy.md)

## Objectif et périmètres

Chaque réglage possède : `key` stable, schéma/type/units, valeur par défaut, documentation, groupe, scope, révision, origine, état calculé, capacité OS/WebStack, dépendances, niveau d'autorisation, secret ou non, classe d'impact, validateur et politique de reprise.

**Hiérarchie ciblée** : valeurs du produit → politique globale administrateur → serveur → organisation/revendeur → plan d'hébergement → compte → site/application → paramètre individuel autorisé. Un niveau inférieur peut surcharger seulement si son parent délègue la clé et si la valeur respecte ses contraintes. Les limitations globales de sécurité s'appliquent toujours ; un « mode Expert » change l'affichage, jamais les droits effectifs.

Les secrets sont des références à un stockage protégé, non des valeurs lisibles dans les réponses API, journaux, exports, vues, backups accessibles ou manifests.

## Catalogue de familles configurable

| Famille | Réglages exposés | Autorité et limites |
|---|---|---|
| Interface générale | Langue, fuseau horaire, densité, thème clair/sombre, widgets, annonces | Préférences utilisateur ou organisation ; aucune modification de droits |
| Branding / white-label | Logo, palettes, favicon, nom, domaine, templates d'email, identité revendeur | Organisation ayant permission, vérification DNS/TLS, pas de partage de cookies |
| Identité et RBAC | Rôles, permissions, sessions, accès API, MFA **facultatif**, paramètres de connexion | Autorité serveur/super-admin ; garde-fous et réauthentification |
| Ports et réseau | IP/IPv6, ports des portails, listeners, noms d'hôtes, reverse proxy | Administrateur système ; maintien de l'ancien accès jusqu'au succès du nouveau |
| WebStack et PHP | Profils Nginx/Apache/Caddy, versions PHP-FPM/FrankenPHP, limites et règles compatibles | Politique du serveur, capacité réelle et isolation tenant |
| Runtimes applicatifs | PHP, Node.js, Python, versions et extensions, déploiement de conteneurs | Comptes/serveurs autorisés ; limites cgroups, images signées et restrictions |
| Bases, DNS et mail | Fournisseurs, quotas, zones, boîtes, stockage, sauvegardes | Service natif/compte, sans élévation de privilège |
| Sécurité système | Firewall, SELinux/AppArmor, SSH, SFTP, verrouillage, audit | Administrateur ; **pas de désactivation implicite des contrôles** |
| Sauvegardes | Destinations, rétention, chiffrement, planifications et tests de restauration | Permissions serveur/compte, règles anti-effacement |
| Jobs et mises à jour | Créneaux, canaux stable/beta, retries, verrous, alertes | Permissions dédiées et vérification des signatures |
| Modules et extensions | Activation, version, paramètres, sources de packages, contrats et permissions | Confiance signée ; Core autonome sans extension |
| Connectivité Hub | Enregistrement volontaire, droits premium, vérification de versions, données techniques minimales, support et marketing **séparés** | Consentements distincts ; Core gratuit indépendant |
| Licences commerciales | État des droits, échéances, dernière preuve, délai hors ligne 60 jours, alertes | État **affiché**, politique d'émission de droits fixée par éditeur ; le client ne peut prolonger seul sa licence |

Les réglages de performance ne doivent pas exposer des variables arbitraires permettant une commande shell ou la suppression de l'isolation.

## Cycle de changement et garanties Q47

1. `DRAFT` — modification locale, diff en lecture seule, auteur et périmètre.
2. `PLAN` — compiler les changements selon les adaptateurs de l'OS, dépendances, conflits, propriétés de listeners, permissions et compatibilité.
3. `PREFLIGHT` — vérifier ressources, syntaxe, certificats, sauvegardes préexistantes et préconditions.
4. `SNAPSHOT` — sauvegarder configuration et données pertinentes avant mutation ; chiffrer et définir restauration et limites.
5. `APPLY` — verrouiller les ressources, préparer un ensemble versionné, appliquer en étapes idempotentes ; journal d'opérations durable.
6. `VERIFY` — contrôler statut systemd, santé du panneau, disponibilité locale et effective des services.
7. `COMMIT` — enregistrer version appliquée/audit, publier état et notifications.
8. `RECOVER` — si échec, restaurer ce qui est réversible et proposer une compensation explicite pour les effets non réversibles.

Les changements purement visuels peuvent s'appliquer immédiatement. Une modification de ports, firewall, WebStack, droits ou de storage exige au minimum PLAN/PREFLIGHT/SNAPSHOT/APPLY/VERIFY. Préserver un accès d'administration de secours lors des modifications réseau ; aucune garantie de rollback global d'une suppression de base/installation de paquet.

## Nouveaux réglages Q56–Q60

Le Core propose une politique de canaux **Stable/Beta/Dev**, avec contrôle d'accès et compatibilité (Q57) ; comptes locaux et SSO/OIDC facultatif avec MFA administrateur optionnel (Q58) ; conservation par catégorie et plafonds légaux/de sécurité (Q59). Prestataires de paiement et offres achat définitif/abonnements/essais/coupons/packs/options relèvent du **Hub**, pas du Core (Q56/Q60). Tous ces réglages restent à implémenter. [Spécification](../00-project-control/commerce-identity-release-policy.md).

## Paramètres nouveaux liés à Q61–Q70

Contrôle des canaux/signatures/approbations de publication (Q61) ; installation DEB/RPM vérifiée (Q62) ; DNS/mail par fournisseur et capacité (Q63–Q64) ; destinations, chiffrement, rétention, réplication et immutabilité des backups (Q65) ; réauthentification et approbation supplémentaire (Q66) ; politiques de groupes et clusters (Q67) ; seuils/destinataires d'alertes (Q68) ; propriété des IP/ports et profils par site (Q69) ; édition visuelle versionnée (Q70). Les modifications sensibles restent soumises à PLAN/VALIDATE/SNAPSHOT/APPLY/VERIFY/RECOVER. [Détails](../00-project-control/infrastructure-decisions.md).

## Politique Q71–Q80 et choix par site

Le registre de configuration devra afficher l'autorité du prestataire de clés et la rotation, les services Linux existants admissibles à l'adoption, les pilotes DNS et mail vérifiés, les sauvegardes 3-2-1 et leurs tests, les demandes d'approbation et secours, les groupes de serveurs, les exports Prometheus/OpenTelemetry et les widgets déclaratifs approuvés. **Q79** ajoute une `recommended_webstack` **par site** et une opération `webstack.planSwitch(site_id,target_profile,revision)` distincte du choix initial, soumise à PLAN/VALIDATE/SNAPSHOT/STAGE/VERIFY/RECOVER ; ne pas changer les autres vhosts. [Détails](../02-architecture/site-webstack-advisor.md).

## Réglages de site Q81–Q90

Proposer des clés typées/allowlistées : `site.webstack.profile`, `site.webstack.recommendation_revision`, `site.php.version`, `site.php.extensions`, `site.php.fpm_limits`, `site.tls.mode`, `site.tls.acme_challenge`, `site.deploy.git_ref`, `site.staging.policy`, `account.database.drivers`, `account.cache.drivers`, `account.ssh.access`, `mail.domain.filters`, `plan.quota.*` et `site.restore.scope`. Aucune valeur non autorisée ne peut contourner le plan/serveur. Les champs sont des exemples de contrat, non une API implémentée.

Q82 exige pour un changement de WebStack : `PLAN → PREFLIGHT → SNAPSHOT → STAGE → TEMP_ROUTE_TEST (si disponible) → CUTOVER (progressif si sûr) → VERIFY → FINALIZE/RECOVER`. Les fenêtres de maintenance, notifications, interruptions possibles et limites de rollback sont affichées. Q90 exige le même contrôle avant restauration/clonage vers staging. [Cycle d'hébergement](website-lifecycle.md) et [Q81–Q90](../00-project-control/decisions-q81-q90.md).

## API cible et critères de validation

Opérations envisagées : `config.readEffective(scope)`, `config.plan(changes,expected_revision)`, `config.apply(plan_id,idempotency_key)`, `config.history(resource)`, `config.recover(generation_id)`. Versionner les schémas ; erreurs ciblées `PERMISSION_DENIED`, `POLICY_LOCKED`, `CAPABILITY_UNAVAILABLE`, `CONFLICT`, `PLAN_STALE`, `PARTIAL_RECOVERY`.

Tests : aucune escalade via scope enfant ; permission refusée sur CLI et API ; rejeter révision obsolète ; config invalide non activée ; conflit port détecté ; nouveau port testé avant ancien retiré ; panne après snapshot ; compensation partielle explicite ; drift détecté sans écraser les fichiers externes ; permissions/valeurs visibles sans divulgation de secrets.

**Statut : entièrement spécifié, aucun Configuration Engine exécutable dans le dépôt actuel.**
