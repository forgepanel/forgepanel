<!-- forgepanel-doc id=FP-00-DECISIONS revision=14 status=documented -->
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

| ADR-060 | PHP maintenus, alertes EOL et migrations planifiées (Q91 C) | Inventaire PHP/extension et alertes par site ; PHP du panneau distinct ; migration non destructive |
| ADR-061 | PHP-FPM isolé par site avec confinement Linux avancé (Q92 D) | Pools/identités/quotas séparés et capacités SELinux/AppArmor/cgroups certifiées ; pool seul insuffisant |
| ADR-062 | Git Deploy manuel ou webhook validé, politique par site (Q93 C) | Contrôle des webhooks/refs, idempotence, RBAC et journaux expurgés |
| ADR-063 | Staging privé par site, anonymisation/secrets/rétention/audit (Q94 D) | Envois mail/webhooks réels neutralisés, approbation de copie et purge contrôlée |
| ADR-064 | Autorités ACME multiples, DNS-01 et renouvellement contrôlé (Q95 C) | Pilotes DNS, preuve du domaine, wildcard, secrets protégés, alertes |
| ADR-065 | Plusieurs moteurs de données par compte avec droits/quotas séparés (Q96 D) | MariaDB/MySQL, PostgreSQL et Redis/Valkey optionnels ; SQL Core isolé |
| ADR-066 | SSH limité par clés et plan, révocation/expiration/audit (Q97 C) | Identités Linux/chemins restreints ; aucun terminal web implicite |
| ADR-067 | Webmail interchangeable selon serveur/fournisseur et politiques domaine (Q98 C) | Pilotes qualifiés, isolation boîtes, webmail/quarantaine compatibles |
| ADR-068 | Quotas soft/hard, grâce et rallonge administrateur (Q99 D) | Autorisation explicite, limites réelles non contournables, trace et expiration |
| ADR-069 | Migration/restauration inter-serveurs sécurisée et auditée (Q100 D) | Préflight OS/WebStack/PHP/DB, transfert chiffré, staging et secrets tournés, reprise |

| ADR-070 | Exception PHP EOL temporaire avec migration prévue (Q101 C) | Dérogation par administrateur, site/échéance/révision et audit ; pas d'exception permanente implicite |
| ADR-071 | Profils d'isolation sélectionnables selon capacités Linux certifiées (Q102 C) | Héritage plan/site, refus des profils indisponibles ; FPM seul n'est pas confinement complet |
| ADR-072 | Git Deploy par site ET environnement avec approbation configurable (Q103 C) | Staging/production, ref, webhook signé, permissions et politique d'autorisation séparées |
| ADR-073 | Copie staging de données sensibles avec approbation spéciale (Q104 D) | Profils fichiers/schéma/anonymisés, secrets distincts, rétention, purge et audit |
| ADR-074 | ACME multi-autorités, retries bornés, alertes et secours (Q105 C) | Alternatives préautorisées, DNS-01 compatible, préserver certificat sain avant remplacement |
| ADR-075 | DB mutualisée/dédiée selon plan + cluster/réplication facultatifs (Q106 D) | Pilotes certifiés et isolation tenant ; aucun cluster implicite au Core |
| ADR-076 | SSH restreint/IP autorisées, accès temporaires et certificats compatibles (Q107 C) | Autorité SSH certifiée, durée/révocation/audit ; ni root ni terminal web implicite |
| ADR-077 | Webmail recommandé après tests de sécurité/compatibilité/maintenance (Q108 D) | Aucune présomption Roundcube/SnappyMail ; choix serveur/fournisseur/domaine |
| ADR-078 | Grâce et plafonds de quotas par plan et ressource (Q109 C) | Seuils/échéances et allocations administrateur Q99 ; limites physiques non franchissables |
| ADR-079 | Pré-synchronisation et bascule avancée conditionnelle (Q110 D) | Test staging et DNS/proxy, réplication/failover uniquement si application/infrastructure compatibles ; pas de zéro downtime garanti |

| ADR-080 | AGPL-3.0 + commerciale, variante après revue juridique (Q111 C) | Choix stratégique maintenu ; only/or-later et texte commercial non sélectionnés, aucun LICENSE final |
| ADR-081 | CLA électronique avec vérification des pouvoirs individuels/entreprises avant fusion (Q112 C) | Texte, identité juridique, signataires, preuves d'accord et autorisation de double licence à valider |
| ADR-082 | Pools de licences par organisation, transferts et remplacement serveur (Q113 D) | Plafonds, affectations et reprise auditables ; aucun privilège Linux |
| ADR-083 | Partenaires : revue de chaque version, maintenance/sécurité et retrait (Q114 C) | Vérification manuelle continue, provenance, signatures et réponse aux incidents |
| ADR-084 | Paiements : adaptateurs sandbox puis choix par marché (Q115 D) | Prestataires réels, pays, monnaies et taxes non présumés |
| ADR-085 | Rétention par catégorie et juridiction sous loi (Q116 C) | Durées min/max, gel légal, purge et audits configurables ; pas de chiffres inventés |
| ADR-086 | Révocation premium selon motif sans couper Core (Q117 C) | Sécurité/fraude/remboursement/expiration ; révocation connue ≠ 60 jours hors ligne automatiques |
| ADR-087 | Signalement privé GitHub + email sécurité vérifié, triage/notifications (Q118 C) | Configurer et vérifier les deux canaux avant diffusion ; aucune adresse inventée |
| ADR-088 | Première version testable : installateur/CLI/wizard/identité/PG + site PHP/domaine/HTTPS (Q119 B) | Preuve VM/HTTP/TLS, diagnostics/récupération et permissions, pas les modules avancés |
| ADR-089 | Ordre : sources → Symfony/PG → installateur → premier site/VPS → ABI → Hub (Q120 D) | Dépendances et critères de sortie dans la roadmap ; le Hub ne bloque pas le MVP Core |

| ADR-090 | Premier OS par comparaison des prérequis et VM (Q121 D) | Aucun OS choisi sans essais ; qualification réelle par distribution |
| ADR-091 | Première WebStack après tests compatibilité et sécurité (Q122 D) | Aucun profil imposé ; conseil indépendant par site (Q79) conservé |
| ADR-092 | MVP : DNS externe et HTTPS ACME HTTP-01 (Q123 A) | Challenge port 80 et certificat HTTPS vérifiés ; DNS natif/DNS-01 restent ultérieurs |
| ADR-093 | MVP : admin local et rôle gestionnaire de site (Q124 B) | Identité permanente, récupération, sessions et RBAC ; MFA facultatif |
| ADR-094 | MVP : monitoring VPS et mises à jour/paquets OS contrôlés (Q125 B) | PLAN/préflight/autorisation/audit/récupération ; jamais de shell root arbitraire |
| ADR-095 | MVP : backup config panneau + fichiers site PHP et restauration testée (Q126 B) | Intégrité/reprise réelle ; cohérence PG nécessaire au panneau, sans exiger 3-2-1 au MVP |
| ADR-096 | Tests internes puis bêta privée autorisée après prérequis (Q127 B) | Tests VM, revue des obligations de distribution, canal sécurité et approbation propriétaire |
| ADR-097 | Licences premium transférables en self-service et récupération manuelle (Q128 D) | Preuve d'identité/possession, plafond, audit et anti-double affectation ; Hub ultérieur |
| ADR-098 | Partenaires : obligations/délais contractuels, alertes et retrait (Q129 C) | Chaque version vérifiée, responsabilité et escalade ; aucun délai inventé |
| ADR-099 | Responsable sécurité + suppléant et triage coordonné (Q130 C) | Rôles/contacts réellement vérifiés avant bêta, pas de nom/adresse implicite |

| ADR-100 | VM locales/CI, snapshots, pannes simulées et rapports OS (Q131 D) | Comparaison reproductible avant choix OS, SKIP ≠ PASS et tests VM réels |
| ADR-101 | WebStack : charge, maintenance, reprise et seuils éliminatoires (Q132 D) | Aucun profil initial choisi ; fuite tenant, bypass .htaccess et collision ports éliminatoires |
| ADR-102 | DNS externe : diagnostiquer A/AAAA, port 80, HTTP-01, HTTPS (Q133 C) | Vérification IP/vhost, challenge et certificat, sans imposer DNS natif |
| ADR-103 | OS updates avec plan impact, sauvegarde, santé et récupération (Q134 C) | Permissions et idempotence ; pas de shell root libre |
| ADR-104 | MVP backup local chiffré + destination distante facultative (Q135 B) | Config panneau/fichiers PHP, restauration vraie ; remote et 3-2-1 ultérieurs |
| ADR-105 | Gestionnaire site : PHP/domaines/TLS/fichiers/SFTP et restauration limitée (Q136 C) | RBAC/quotas par site, aucune gestion de paquets root ni site tiers |
| ADR-106 | Bêta privée par vagues, suspension et récupération (Q137 D) | Invitations/conditions, canal bugs/versions, droits logiciels déjà octroyés préservés |
| ADR-107 | Transferts premium avec preuve crypto et seconde validation selon risque (Q138 D) | Antifraude, audit, serveur perdu en secours, Hub après ABI |
| ADR-108 | Partenaires : gravité, alertes auto, escalade et retrait (Q139 C) | Obligations contractuelles et revue manuelle par version Q114/Q129 |
| ADR-109 | Vulnérabilités : triage, correctifs, avis/communication coordonnés (Q140 C) | Responsable + suppléant et canaux privés réels Q118/Q130 |

| ADR-110 | Pilotes VM locales/cloud et CI avec rapports communs (Q141 D) | VM système réelles, snapshots, pannes, preuves OS, SKIP ≠ PASS |
| ADR-111 | Budgets de performance par application et régressions de versions (Q142 D) | Benchmarks comparables, seuils configurables ; veto sécurité/récupération Q132 |
| ADR-112 | Assistant DNS : proposer enregistrements et revérifier (Q143 C) | A/AAAA, 80/HTTP-01 et 443/TLS, **pas** d'édition automatique chez le fournisseur |
| ADR-113 | Mise à jour OS par serveur, orchestration multi-serveurs future (Q144 D) | Plan d'impact, backup, vérification santé/reprise, autorisation et audit |
| ADR-114 | Coffre et récupération de clés backup, KMS externe/autorités multiples facultatifs (Q145 D) | Backup chiffré local/restaurable, copie de clé protégée hors panne commune, autonomie Core |
| ADR-115 | SFTP sans shell, expiration/révocation, quotas et audit (Q146 C) | Par site/compte, chemins canoniques, accès inter-tenants interdits |
| ADR-116 | Bêta par vagues avec seuils de santé et pause/récupération (Q147 C) | Pas de données effacées, télémétrie Q6 consentie ; Core fonctionnel hors Hub |
| ADR-117 | Identité serveur premium clés/challenge, anti-rejeu/org et secours manuel (Q148 C) | Transfert Hub après ABI, seconde approbation selon risque Q138 conservée |
| ADR-118 | Partenaires : gravité, délais contractuels, escalade/alertes/retrait (Q149 C) | Revue humaine de chaque version, aucun SLA numérique inventé |
| ADR-119 | Avis sécurité signés/historisés, notification et divulgation coordonnée selon risque (Q150 D) | Responsable/suppléant, canaux vérifiés, pas de publication automatique d'exploits |

| ADR-120 | QEMU/KVM local premier pilote puis VM cloud (Q151 A) | Garder ABI multi-pilotes Q141 ; ne pas certifier la CI si KVM absent |
| ADR-121 | Rapports VM signés/provenance/snapshots/historique (Q152 C) | Matrice interne, PASS/FAIL/SKIP explicites ; pas de publication publique automatique |
| ADR-122 | Blocage de régression selon gravité, exception performance approuvée (Q153 C) | Budgets par application, audit et limite ; **aucun veto sécurité/récupération contournable** |
| ADR-123 | DNS HTTP-01 : familles d'IP réellement publiées seulement (Q154 C) | A et/ou AAAA validés individuellement ; ne pas imposer IPv6 absent |
| ADR-124 | Mise à jour/reboot OS par serveur et approbation/backup/santé/reprise (Q155 C) | Aucune commande root arbitraire, multi-serveurs plus tard |
| ADR-125 | Clé de secours, vérification périodique et restauration isolée (Q156 C) | Backup « récupérable » seulement après essai réel ; KMS/multi-gardiens optionnels |
| ADR-126 | Gestion clé publique SFTP par compte/site, expiration/audit/validation (Q157 C) | Pas de clé privée collectée, shell interdit, quotas et RBAC imposés |
| ADR-127 | Bêta : santé locale, rapports manuels et diagnostic minimal opt-in par cohorte (Q158 C) | Consentements Q6 séparés, pause par seuils, pas de télémétrie forcée |
| ADR-128 | Transfert premium suspect : serveur perdu, répétition, incohérence org ou compromission (Q159 C) | Q138 approbation conditionnelle et Q148 challenge, secours manuel Hub |
| ADR-129 | Avis sécurité signés FR/EN humains + structurés machine (Q160 C) | Notifications configurables, contenus sensibles protégés, pas de standard avancé imposé |

| ADR-130 | Runners KVM éphémères isolés, images figées, quotas et nettoyage automatique (Q161 C) | Q151 local d'abord, puis pilotes cloud. Vérifier capacités KVM, empreintes images/commits, ressources et nettoyage des secrets ; conserver les preuves signées hors runner. |
| ADR-131 | Stockage privé immuable des rapports signés avec historique, rétention et contrôle d'accès (Q162 B) | Q152 rapports internes : vérifier signatures, provenance, snapshots, versions, historique et RBAC ; seconde réplication indépendante (option C) non adoptée. |
| ADR-132 | Exceptions de performance approuvées selon gravité, séparation des rôles, portée, expiration et révision (Q163 C) | Q153/Q142 uniquement budgets de performance non critiques : approbateur différent du demandeur selon politique, révocation et audit. Veto sécurité, isolation et récupération Q132 non dérogeables. |
| ADR-133 | Contrôles DNS locaux et une sonde externe indépendante (Q164 B) | Q154 : vérifier uniquement A/AAAA réellement publiés sur port 80/HTTP-01 et HTTPS ; la sonde externe doit être bornée, autorisée et protégée contre SSRF. Pas de réseau de sondes multiples (option C). |
| ADR-134 | Réparation non destructive bornée, checkpoints et validation humaine des opérations risquées (Q165 C) | Q155 : actions système explicites allowlistées, tentatives et délais plafonnés, audit/état santé ; pas de shell root arbitraire ni de rollback destructif sans approbation. |
| ADR-135 | Restaurer chaque sauvegarde sur environnement isolé ; vérifications profondes périodiques et exercices de panne selon criticité (Q166 C) | Q156 : sauvegarde récupérable seulement si périmètre complet restauré isolément PASS, clé de secours protégée accessible ; essais périodiques perte hôte/clé/panne sans détruire les vraies clés. |
| ADR-136 | SFTP par clé publique vérifiée, expiration, rotation, algorithmes autorisés, audit et contrôle sensible (Q167 C) | Q157/Q146 : gestionnaire limité à ses sites ; possession de clé, quotas, confinement canonique, révocation, validation des opérations sensibles ; jamais de clé privée cliente ni shell. |
| ADR-137 | Consentements séparés, seuils par catégorie/cohorte, agrégation, expurgation et protection anti-réidentification (Q168 C) | Q158/Q6 : pas de télémétrie forcée. Seuils configurables par donnée/cohorte, minimisation et protection contre recoupements ; santé locale et rapports manuels préservés sans Hub. |
| ADR-138 | Transferts premium simples automatisés sous règles de risque versionnées, seconde approbation et secours sécurisé (Q169 C) | Q159/Q138/Q148 : identité, droits, org et challenge nonce vérifiés ; revue humaine et gel du transfert premium en cas de répétition, source perdue, incohérence ou compromission. Pas de moteur arbitraire par produit (Q159 D). |
| ADR-139 | Avis sous JSON Schema versionné, signé, validé, avec rendus FR/EN synchronisés et historique (Q170 B) | Q160/Q150 : source canonique commune aux formes structurée et humaine, destinataires autorisés, notifications configurables et données sensibles protégées ; interopérabilité avancée option C non imposée. |
| ADR-140 | Orientations produit Q171–Q220 explicitement approuvées (47 D ; Q174, Q194, Q200 C) | [Registre canonique des 50 décisions](decisions-q171-q220.md) et [réconciliation conditionnelle](reconciliation-q171-q220.md). Q1–Q170 conservées ; Q221+ ouvertes ; aucun code, test VM, valeur par défaut, fournisseur, API active, pouvoir Hub ou release approuvé par cette ADR. |

## Propositions remplacées ou non résolues

Vue comme frontend principal et Debian seul ont été remplacés par l'interface native Symfony et l'exigence multi-OS ultérieure. Python et Redis restent optionnels. L'enrôlement TOTP existe dans l'archive ; WebAuthn et l'authentification permanente restent futurs. Les anciennes affirmations d'agent fonctionnel, d'installateur complet ou de publication officielle ne sont pas étayées par le dépôt observé.

Toute nouvelle décision précise contexte, alternatives, justification, contrats affectés, validation et décision remplacée. Une exigence évolue par réconciliation explicite, pas par effacement silencieux de l'historique.
