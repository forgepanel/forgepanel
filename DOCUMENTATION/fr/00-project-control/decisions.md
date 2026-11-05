<!-- forgepanel-doc id=FP-00-DECISIONS revision=5 status=documented -->
# Registre de décisions

[English](../../en/00-project-control/decisions.md) · [Pilotage](README.md)

Les identifiants sources renvoient à l'[état initial](../19-audits-risks/baseline.md). Une décision retenue comme référence de conception ne prouve pas son implémentation.

| ID | Décision et autorité | État / conséquence |
|---|---|---|
| ADR-001 | ForgePanel est le nouveau produit ; WCP360 est historique (SRC-02) | Identité confirmée ; aucun héritage automatique du code, de la licence ou du commerce WCP360 |
| ADR-002 | Symfony/PHP + Twig/UX ; Go pour le système ; PostgreSQL (SRC-02, manifeste SRC-03) | Référence de conception ; l'archive contient Twig mais pas les dépendances UX/Tailwind/Messenger installées |
| ADR-003 | Multi-OS dès le départ (demande explicite du propriétaire, SRC-02) | Exigence : Debian 12/13 ; Ubuntu et AlmaLinux ; matrice d'archive 24.04/26.04 et 9/10 ; aucune certification |
| ADR-004 | Moteurs web composables, cinq identifiants de profils (SRC-02/03) | Spécifié ; sélection présente, provisionnement des services absent |
| ADR-005 | Installation en une commande, puis wizard et récupération CLI (propriétaire, SRC-02) | Résultat obligatoire ; non livré par `install plan` |
| ADR-006 | Jeton bootstrap plutôt que mot de passe Linux dans le navigateur (SRC-02/03) | Référence de sécurité conservée ; le super-admin applicatif n'est pas root Linux |
| ADR-007 | PostgreSQL porte la transaction du bootstrap web (SRC-03) | Implémentation d'archive remplaçant l'intégration du jeton fichier v0.6 ; SQL non vérifié |
| ADR-008 | Ports directs 8447/8446 et hôtes de portails distincts (SRC-02/03) | Valeurs du prototype ; suggestion 446/447 non retenue ; USER fermé ; les ports n'isolent pas les cookies |
| ADR-009 | Documentation bilingue, changelog unique, quatre branches permanentes (propriétaire, SRC-01) | Régit ce lot ; créer une branche n'autorise ni release ni déploiement |
| ADR-010 | Politique du runtime applicatif | Ouverte : l'archive accepte PHP >=8.2 ; la préférence PHP 8.4 ne certifie pas une politique de paquets sur six OS |
| ADR-011 | Licence et contributions | **AGPL-3.0 + licence commerciale (Q48)** ; variante only/or-later et texte commercial à approuver ; provenance et droits tiers à vérifier avant LICENSE |
| ADR-012 | Outil documentaire limité à la bibliothèque standard Python | Nouveau choix d'outillage borné ; ne rend pas Python obligatoire pour le produit |
| ADR-013 | MFA administrateur facultatif (décision explicite du propriétaire, 2026-11-05) | Premier compte sans obligation TOTP ; activation immédiate ou différée, réauthentification sensible ; code v0.7 encore bloquant à corriger lors de son import. |
| ADR-014 | ForgePanel-Hub, extension éditeur privée détachée dans `yyogas/forgepanel-hub` | Même Core standard avec/sans Hub ; ABI générique encore absente ; aucune injection de PHP privé ni accès root. |

| ADR-015 | Core complet gratuit, services premium et support (Q2, Q50 B) | Premium : plugins spécialisés, services cloud/managés, offres partenaires et support ; aucun péage sur le Core AGPL |
| ADR-016 | Publics par étapes (Q3, Q54 D) | Hébergement mutualisé + administration VPS en premier ; développeurs/conteneurs puis revendeurs et fonctions avancées, selon validation |
| ADR-017 | PHP, Node.js, Python et conteneurs clients (Q4, Q51 C) | **Docker et Podman** via pilotes distincts ; sécurité et compatibilité OS à tester ; séparés du runtime du panneau |
| ADR-018 | White-label (Q5, Q55 A) | **Une seule marque par organisation** ; logo, domaine, thème, emails et portail configurables dans ses permissions ; pas de multimarque par organisation |
| ADR-019 | Enregistrement Hub et communications séparés et consentis (Q6) | Autorisations distinctes : inscription, droits premium, versions, diagnostics, marketing ; aucune collecte implicite |
| ADR-020 | 60 jours hors ligne + comportement terminal (Q7, Q52 A) | Au-delà, **bloquer les nouvelles opérations premium**, préserver l'existant et toute donnée ; ni arrêt de sites ni blocage du Core. Expiration/révocation explicite à préciser |
| ADR-021 | Catalogue officiel et partenaires (Q8, Q53 B) | **Candidature + vérification manuelle** avant approbation ; contrôle des versions/signatures, retrait et traitement des incidents |
| ADR-022 | Modification sensible : plan, validation, sauvegarde et récupération (Q47) | Config Engine cible ; aucune garantie de rollback OS/SQL universel |

| ADR-023 | Accord de contribution (Q49 A) | **CLA** autorisant la double licence, avec vérification et conservation des preuves ; texte juridique/entité/signature encore à décider |
| ADR-024 | Protection commerciale des modules et abonnements (précision propriétaire) | Droits et contrôles de paiement sur services/modules premium indépendants, jamais restriction additionnelle des libertés du Core AGPL ; revue juridique du couplage Hub/plugins |

| ADR-025 | Paiement multi-prestataires (Q56 C) | Pilotes indépendants côté Hub ; aucun prestataire ni secret choisi ; achats validés par callbacks authentifiés et dédoublonnés |
| ADR-026 | Canaux Stable, Beta, Dev (Q57 C) | Déploiements progressifs, signature, contrôles de compatibilité et récupération ; politique d'auto-update encore ouverte |
| ADR-027 | Comptes locaux et SSO/OIDC facultatif (Q58 C) | Authentification locale et récupération conservées ; identités externes permissionnées, MFA toujours facultatif |
| ADR-028 | Rétentions par catégorie (Q59 C) | Durées configurables dans les limites de sécurité et légales ; périodes exactes à définir |
| ADR-029 | Achat définitif + abonnements + essais/coupons/packs/options (Q60 C) | Modèle commercial Hub ; droits issus d'événements de paiement vérifiés, pas d'une redirection navigateur |

| ADR-030 | CI/CD signé + anti-rétrogradation + approbations (Q61 C) | Artefacts et métadonnées signés, racines de confiance protégées et validation avant publication ; système à réaliser |
| ADR-031 | Installation universelle + dépôts DEB/RPM signés (Q62 C) | Bootstrap d'origine vérifiée, installateur reprenable et paquets adaptés à chaque OS cible ; pas d'installateur disponible |
| ADR-032 | DNS local + fournisseurs externes par drivers (Q63 C) | Autorité par zone, validation des enregistrements et changement de fournisseur contrôlé |
| ADR-033 | Mail natif + fournisseurs externes (Q64 C) | Services locaux/externes via pilotes, séparation des comptes et vérification DNS/TLS |
| ADR-034 | Sauvegardes distantes répliquées, chiffrées, immuables, récupération (Q65 D) | Restaurations testées, limites de stockage et objectifs de reprise mesurés |
| ADR-035 | Réauthentification sensible et approbation supplémentaire configurable (Q66 C) | MFA administrateur toujours facultatif ; policy d'approbation, audit et mode secours |
| ADR-036 | Multi-serveurs et HA/clustering/DR (Q67 D) | Cible par phases ; pas de cluster certifié ni de dépendance au Hub |
| ADR-037 | Monitoring local + alertes email/webhooks + intégrations externes (Q68 C) | Règles configurables et maîtrise des données exportées |
| ADR-038 | WebStacks par site et frontaux selon IP/port (Q69 D) | Listeners exclusifs, vérification TLS, `.htaccess` et configurations planifiées ; Q79 précise la recommandation et le changement **par site** |
| ADR-039 | Éditeur visuel avec widgets/navigation et marque unique (Q70 D, Q55 A) | Composants approuvés, thème/historique et permissions, sans code arbitraire |

| ADR-040 | Clés sécurisées, anti-rétrogradation et rotation (Q71 C) | Signature CI avec service de clés/KMS/HSM approprié, métadonnées de confiance, rotation et récupération ; fournisseur non arrêté |
| ADR-041 | Installation vierge + adoption contrôlée de services existants (Q72 C) | Inventaire en lecture seule, plan, conflits, confirmation, backup/restore ; aucune prise de possession silencieuse |
| ADR-042 | DNS multi-pilotes et recommandation locale après tests (Q73 D) | Aucun moteur DNS local imposé ; détecter capacités/certifier avant recommandation |
| ADR-043 | Postfix + Dovecot premier pilote mail et externes (Q74 C) | Backend natif initial, fournisseurs/relais par adaptateurs, sécurité et compatibilité à certifier |
| ADR-044 | Sauvegarde 3-2-1, restauration testée, réplication configurable (Q75 C) | Politique cible, nombre/cadence/destinations selon capacités, immutabilité Q65 maintenue |
| ADR-045 | Approbation par action avec secours audité (Q76 C) | Réauthentification, contrôle de séparation des rôles, méthode de récupération sûre ; MFA facultatif maintenu |
| ADR-046 | Multi-serveurs puis HA et orchestrateurs externes par modules (Q77 D) | Capacité progressive, sans dépendance au cluster pour premiers sites |
| ADR-047 | Prometheus + OpenTelemetry via pilotes (Q78 C) | Exportateurs/capacités configurables, filtrage et consentement aux sorties |
| ADR-048 | WebStack recommandée **par site**, modifiable après création (Q79 D, précision propriétaire) | Choix non imposé au provisionnement, changements futurs avec PLAN/VALIDATE/STAGE/HEALTH/RECOVER ; préserver `.htaccess` et listeners |
| ADR-049 | Widgets officiels/partenaires et widgets déclaratifs (Q80 C) | Sources autorisées, manifests, RBAC, rendu sûr, une marque par organisation, aucun code arbitraire |

| ADR-050 | Conseiller WebStack application/sécurité/ressources/listeners (Q81 C) | Recommandation par site selon .htaccess, PHP, OS et isolation ; refus incompatibles |
| ADR-051 | Changement WebStack avec route test/bascule progressive si compatible (Q82 D) | Plan, snapshot, notifications, maintenance, TLS/règles et récupération ; aucune garantie zéro interruption |
| ADR-052 | PHP par site avec extensions/PHP-FPM/quotas (Q83 C) | Runtime panneau séparé et pools/paramètres validés par serveur/plan/tenant |
| ADR-053 | ACME, certificats importés, DNS-01, wildcards et renouvellement (Q84 C) | Propriété du domaine, fournisseur DNS compatible, secrets et alertes |
| ADR-054 | Fichiers/SFTP + Git Deploy + staging/preview/backup/rollback (Q85 C) | Migration SQL non automatiquement réversible ; aucune obligation blue-green/canary |
| ADR-055 | MariaDB/MySQL, PostgreSQL et Redis/Valkey facultatifs (Q86 D) | Pilotes tenant isolés ; cache/queues optionnels et PostgreSQL du panneau distinct |
| ADR-056 | File manager/SFTP + SSH limité aux comptes autorisés (Q87 B) | Scopes Unix, chemins sûrs, quotas, pas de terminal web implicite |
| ADR-057 | Email protégé, webmail, quarantaine, règles/rapports par domaine (Q88 C) | SPF/DKIM/DMARC/TLS, antispam/AV et autorisations par boîte/domaine |
| ADR-058 | Plans et quotas hérités avec alertes/usage (Q89 C) | Stockage, domaines, boîtes, DB, CPU/RAM/PHP/processus avec limites effectives |
| ADR-059 | Restauration sélective, clonage staging, retour contrôlé entre environnements (Q90 D) | Permissions, sauvegardes cible, secret/URL séparés, tests de récupération |

## Propositions remplacées ou non résolues

Vue comme frontend principal et Debian seul ont été remplacés par l'interface native Symfony et l'exigence multi-OS ultérieure. Python et Redis restent optionnels. L'enrôlement TOTP existe dans l'archive ; WebAuthn et l'authentification permanente restent futurs. Les anciennes affirmations d'agent fonctionnel, d'installateur complet ou de publication officielle ne sont pas étayées par le dépôt observé.

Toute nouvelle décision précise contexte, alternatives, justification, contrats affectés, validation et décision remplacée. Une exigence évolue par réconciliation explicite, pas par effacement silencieux de l'historique.
