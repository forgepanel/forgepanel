<!-- forgepanel-doc id=FP-10 revision=17 status=documented -->
# Modèle de sécurité et signalement

[English](../../en/10-security/README.md) · [Index](../README.md)

## Actifs, acteurs et frontières

Protéger privilèges Linux, données clientes, identifiants SQL, clés MFA/chiffrement, autorisations de setup, autorité de signature et intégrité de l'audit. Considérer appelants réseau anonymes, code client hostile, plugins compromis, entrées non fiables et interruptions privilégiées. Un processus déjà compromis comme utilisateur applicatif peut employer ses droits SQL ; le drapeau d'environnement bootstrap n'est pas une sandbox contre cet attaquant.

| Frontière | Exigence |
|---|---|
| Navigateur → Symfony | HTTPS vérifié, hôte/origine de confiance exacts, CSRF sur mutations, sessions sûres, limites d'essais, autorisation des ressources |
| Symfony → agent | Canal privé authentifié et versionné ; opérations typées autorisées ; aucune API `exec(command)` |
| Agent → Linux | Moindre privilège, exécuteur borné, chemins sûrs, verrous par ressource, audit système |
| Client → client | Identités/permissions distinctes et limites explicites ; un pool PHP-FPM seul ne suffit pas |
| Artefact → installation | Racine de confiance indépendante, signatures/empreintes vérifiées, anti-retour arrière et rotation sûre des clés |

SRC-03 n'implémente que les contrôles métier du setup et des protections HTTP dans les sources. Durcissement systemd, contrôles obligatoires, isolation client, rotation de secrets en production, connexion/RBAC complets et restauration ne sont pas démontrés.

## Politique MFA facultatif

Le MFA administrateur est **facultatif**, pas une condition de création du premier compte ni d'accès au wizard. Proposer TOTP et, plus tard, WebAuthn ; permettre activation différée, désactivation contrôlée et codes de récupération si activé. Protéger les actions sensibles par réauthentification et autorisations contextualisées. Le code v0.7 encore obligatoire nécessite une correction et des tests.

## Hub, communication et licences commerciales

Conformément à Q6, l'enregistrement Hub est volontaire, les vérifications premium, la recherche de versions, les diagnostics/support et les communications marketing ont des consentements ou bases de traitement distincts. Aucune collecte par défaut de fichiers, emails, bases ou secrets. Selon Q7, la durée hors ligne commerciale est de **60 jours** pour les droits premium éligibles déjà vérifiés, sous réserve des dates contractuelles ; un refus ou une révocation doit être explicite et non destructif pour l'hébergement de base. Voir la [politique produit](../00-project-control/product-policy.md).

## Identité, paiements et conservation (Q56, Q58, Q59)

Les prestataires de paiement sont des pilotes Hub indépendants : webhooks authentifiés et dédoublonnés, jamais de droit accordé par la seule redirection navigateur. L'authentification SSO/OIDC est **facultative**, avec récupération locale sécurisée ; MFA administrateur facultatif. Les rétentions par catégorie restent contraintes par la loi, les audits et les sauvegardes. Ces composants ne sont pas opérationnels.

## Chaîne de confiance et opérations sensibles (Q61, Q65, Q66)

Paquets et métadonnées de publication signés avec racines de confiance protégées, anti-rétrogradation et approbations. Sauvegardes chiffrées, distantes/immuables et récupérables, avec tests de restauration réels. Réauthentification des opérations sensibles et approbation supplémentaire selon politique ; **MFA administrateur facultatif**, non imposé comme prérequis. Ni signature, ni sauvegarde, ni deuxième validation ne remplacent un contrôle de permissions indépendant. [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Clés, adoption et approbations (Q71, Q72, Q76)

La publication signée utilisera une autorité de clés protégée avec rotation et protection anti-rétrogradation (Q71), jamais de clé privée dans le dépôt ou le package. L'adoption d'un service existant (Q72) exige permission, inventaire des ressources, snapshot et refus d'écrasement des configurations non gérées. Les actions sensibles (Q76) peuvent nécessiter un approbateur indépendant ; une procédure locale de secours doit rester auditée. **MFA administrateur toujours facultatif**, et aucun droit d'approval ne remplace RBAC. [Décisions](../00-project-control/decisions-q71-q80.md).

## Isolation des sites, certificats et données — Q81–Q90

La bascule WebStack exige permissions, sécurité des listeners/`.htaccess`, HTTP/TLS et absence de fuite via une route temporaire (Q81/Q82). PHP-FPM par site : versions/directives/extensions allowlistées et quotas réellement appliqués (Q83). ACME/wildcard et import TLS : propriété des domaines, DNS-01 et clés protégées (Q84). Git Deploy/staging, clonage et restauration : aucun transfert implicite de credentials ou de données privées (Q85/Q90). MariaDB/MySQL/PostgreSQL/Redis/Valkey tenant-scopés (Q86), gestionnaire de fichiers/SFTP/SSH limité sans root ni terminal web implicite (Q87), quarantaine/webmail protégés (Q88) et plans/quotas enforceables (Q89). [Détails](../02-architecture/website-lifecycle.md). **Cibles non implémentées.**

## Sécurité des runtimes et migrations (Q91–Q100)

PHP 1 site = identité/pool FPM séparé et confinement Linux réellement vérifié, avec alertes de fin de support et migration planifiée (Q91/Q92). Git manuel/webhook : authentification, anti-rejeu, refs autorisées et logs sans secrets (Q93). Staging : anonymisation, secrets/URLs distincts, suppression des sorties réelles, conservation/audit (Q94). ACME : plusieurs CA/DNS-01 avec preuve de domaine et jetons protégés (Q95). Bases/cache/SSH isolés par compte avec quotas et révocation/expiration (Q96/Q97) ; Webmail et quarantaine visibles uniquement aux détenteurs autorisés (Q98). Grâce quotas bornée ne franchit jamais les limites physiques ni l'isolation (Q99). Migration inter-serveurs : autorisation source et destination, transfert chiffré, rotation des secrets et récupération auditée (Q100). [Référence](../00-project-control/decisions-q91-q100.md). **Non implémenté.**

## Limites de confiance Q101–Q110

Une exception PHP EOL est **temporaire, limitée à un site, autorisée et auditée**, avec migration programmée (Q101) ; elle ne contourne pas les profils d'isolation sélectionnés uniquement parmi les capacités Linux **certifiées** (Q102). Déploiements par site et environnement avec validation/approbation configurable et webhooks anti-rejeu (Q103) ; staging avec données sensibles requiert une **approbation spéciale** et secrets isolés (Q104). ACME multi-autorités avec retries limités, alertes et secours conservant le certificat sain (Q105). Services SQL mutualisés/dédiés avec clusters facultatifs certifiés et isolement inter-tenants (Q106). SSH à clés/IP et accès temporaires/certificats compatibles avec révocation (Q107). Webmail conseillé sur preuve de maintenance et permissions (Q108). Grâce quotas bornée par plan et ressource, jamais au-delà de la sécurité/hôte (Q109). Bascule avancée uniquement lorsque la cohérence source/cible est vérifiée (Q110). [Spécification](../00-project-control/decisions-q101-q110.md). **Tests non réalisés**.

## Critères minimaux de livraison

Ne jamais demander le mot de passe root Linux dans le panneau. Maintenir USER fermé avant validation des autorisations et sessions. Ne pas désactiver SELinux/AppArmor ou le pare-feu pour réussir un test. Éviter les secrets dans URL, logs et artefacts. Exiger diagnostic en lecture seule avant réparation proposée et autorisation explicite avant destruction. Les tests de restauration couvrent les clés, pas seulement SQL/fichiers.

Le verrouillage après cinq essais bootstrap peut servir au déni de service ; restrictions réseau et tests de récupération restent nécessaires. Des vecteurs TOTP validés ne constituent pas un audit cryptographique. Un port n'est pas une frontière d'autorisation.

## Signalement de vulnérabilités retenu (Q118 C)

Avant toute diffusion publique, **configurer et vérifier** deux canaux : signalement **privé sur GitHub** si le dépôt le permet, et **adresse email de sécurité dédiée dont les destinataires sont autorisés**. Les procédures cibles couvrent triage, gravité, accusé de réception, accès restreint, suivi des correctifs et notifications responsables ; aucune adresse, délai contractuel de réponse ou programme de récompense n'est établi ici. Le dépôt et les canaux doivent être vérifiés sur le compte réel avant d'en faire la promotion. [Décisions Q111–Q120](../00-project-control/decisions-q111-q120.md).

## Responsable et suppléant, bêta privée (Q127/Q130)

Q130 C exige un **responsable sécurité identifié et un suppléant**, autorisés à consulter les signalements, trier les incidents, coordonner les correctifs/notifications et escalader pendant une absence. Ces rôles ne sont **pas encore attribués** par ce document. Vérifier réellement le signalement privé GitHub et l'email dédié Q118 avant de laisser des testeurs externes accéder à la bêta privée. Q127 ne justifie ni collecte de secrets clients, ni communication publique de vulnérabilités, ni contournement des obligations de diffusion logicielle. [Décisions](../00-project-control/decisions-q121-q130.md).

## Bêta privée et communication des vulnérabilités — Q137/Q140

La bêta Q137 D utilisera **invitations et conditions acceptées, diffusion par vagues, canal de bugs/versions privé, suspension des accès et récupération documentée**. Suspendre une invitation ou un canal de mises à jour n'autorise ni suppression de données ni retrait automatique des libertés de copies AGPL déjà remises. Q140 C exige, avant une bêta externe, **un responsable et son suppléant effectivement désignés**, triage par gravité, correctifs suivis, avis de sécurité et notifications clients coordonnées, avec les **deux canaux Q118 (GitHub privé + email dédié) testés**. Ces conditions sont spécifiées, **pas installées/configurées**. [Q131–Q140](../00-project-control/decisions-q131-q140.md).

## Protection des accès et avis — Q145–Q150

**Q145 D** : séparer clés/archives de sauvegarde et garder copie de récupération protégée **hors panne commune** ; coffre sécurisé, plusieurs gardiens de récupération selon politique et **KMS externe facultatif**. La perte de toutes les clés doit apparaître comme un risque irréversible, non dissimulé. **Q146 C** : SFTP limité aux sites, sans shell, quotas appliqués et expiration/révocation auditée ; tester symlink et traversée de chemins. **Q147 C** : si une bêta présente un incident critique ou dépasse les seuils de santé configurés, **suspendre les nouvelles vagues** et proposer récupération sans supprimer les données clients ou les droits déjà acquis. **Q148 C** : futur transfert premium par challenge signé, rotation/anti-rejeu et vérification d'organisation, avec secours manuel et approbation conditionnelle Q138. **Q149 C/Q150 D** : obligations partenaires et délais par gravité/contrat, avis de sécurité **signés** et divulgation **coordonnée selon le risque** ; responsable/suppléant et canaux Q118 doivent réellement être assignés/vérifiés. [Décisions](../00-project-control/decisions-q141-q150.md).

## Garde-fous Q151–Q160 — rapports, sauvegardes, accès et avis

**Q152 C** requiert rapport signé/provenance/snapshots/historique de certification mais non une matrice publique obligatoire. **Q153 C** permet exceptions de **performance** selon criticité et autorisation auditée, **jamais** d'exception aux défauts d'isolation, d'accès ou de reprise Q132. **Q154 C** contrôle toutes les familles A/AAAA **effectivement publiées**, sans forcer IPv6 absent. **Q155 C/Q156 C** exigent reboot OS approuvé par serveur, backup utilisable, santé/reprise et clé exportée/vérifiée avant **test de restauration isolé**. **Q157 C** limite la gestion des **clés publiques SFTP** par site à des droits, quotas, expiration et audit, avec revalidation sensible et sans clés privées collectées. **Q158 C** : données de bêta minimisées, consentements Q6 **séparés** et seuils par cohorte, sans collecte imposée. **Q159 C** conserve la seconde approbation Q138 en cas de risque de transfert (perte serveur, répétition, identité/org incohérente, compromission) ; **Q160 C** : avis signés **FR/EN humains et structurés machine**, notifications choisies et secrets protégés, sans format avancé obligatoire ni nouveau canal non vérifié. [Décisions](../00-project-control/decisions-q151-q160.md).

## Signalement et revue

Aucune release de production supportée, adresse privée de signalement ou garantie de réponse n'est établie. Utiliser le signalement privé GitHub seulement s'il est disponible ; sinon demander un canal privé sans publier exploitation ou secrets. Établir ce canal avant distribution publique. La revue sensible doit être distincte de l'implémentation ; aucun relecteur indépendant n'était disponible pour cet audit documentaire. Voir le [registre des risques](../19-audits-risks/README.md).

## Sécurité et exceptions Q161–Q170

Le runner KVM éphémère est isolé, ses secrets nettoyés et les preuves signées Q162 conservées hors VM sur stockage privé immuable contrôlé. Seules les exceptions Q163 de **performance non critique** avec approbation séparée, durée, révision et audit sont permises ; les échecs critiques Q132 ne changent jamais en PASS. Sonde DNS externe Q164 bornée, protection SSRF ; réparations OS Q165 allowlistées, non destructives et à retry plafonné ; backup Q166 jamais récupérable sans restauration isolée intégrale PASS et clés vérifiées ; SFTP Q167 par clé publique autorisée avec possession/rotation/portée site. Q168 évite réidentification et collecte forcée ; Hub Q169–170 protège les transferts premium et avis signés, sans interrompre le Core ni exposer les secrets. [Décisions](../00-project-control/decisions-q161-q170.md).

## Sécurité de l'admission du code source R1

L'import des sources requiert des octets SRC-03 authentifiés selon le registre canonique. Le nouvel outil `stage_source_archive.py` ajoute une **quarantaine non privilégiée**, sans réseau, exécution ni écrasement du Core, après préflight. Défenses : refus des chemins Unicode trompeurs/métadonnées Git/permissions setuid, séparation des étapes validation/copie, répertoire privé, fichiers 0600 et manifeste de provenance. Ces garde-fous ne sont pas une sandbox pour exécuter du code non fiable : aucune archive staging ne doit être exécutée ou déployée. Les plugins/Hub ne peuvent ni autoriser cette opération ni contourner la chaîne R1. [Contrat](../12-development/source-staging.md).

## Revue de sécurité R1 — intégrité et nettoyage de quarantaine

Les fichiers de staging peuvent être contrôlés indépendamment contre **ZIP original + reçu + contenu sur disque**. [Contrat d'audit](../12-development/source-staging-audit.md). Refus : reçus falsifiés, chemins symboliques, hardlinks, permissions non privées ou exécutables, fichier ajouté/supprimé et source modifiée. Le nettoyage d'échec se fait via le **descripteur du parent privé** et vérification `dev/inode` pour ne pas supprimer un autre répertoire si son nom change. Reste une limite : un acteur contrôlant le même UID peut changer les sources **après** l'audit ; l'importeur final doit revalider les octets. Jamais de root, shell générique, import automatique ni élévation Hub.

## Q161 — Sécurité de la préinspection KVM

[`tools/kvm-host-probe`](../14-devops-releases/kvm-host-probe.md) est un outil Go **sans privilèges** : aucune API Linux de commande arbitraire, `ioctl`, accès `/dev/kvm`, exécution de VM, création de fichiers, réseau ou collecte de hostname/IP. Seuls quatre chemins Linux **fixes** sont lus ou inspectés, avec tailles bornées et refus des liens symboliques pour le périphérique KVM. Une détection positive ne permet pas de contourner les gates de sécurité Q132, de restauration Q156 ni les exigences de rapports signés Q152/Q162. L'outil est distinct du daemon privilégié et du Hub.

## Q161 — Refus de toute exécution depuis une admission d'image

L'[outil R3](../14-devops-releases/kvm-image-admission.md) travaille en **lecture seule, non-root et sans QEMU** : les fichiers policy/manifest privés doivent être réguliers et limités, l'image QCOW2 appartient au compte, est sans symlink/hardlink et voit son SHA-256 entier contrôlé via descripteur. Aucun champ JSON ne permet une commande ou argument arbitraire ; réseau/partages/privilèges sont refusés. Un `REVIEW_REQUIRED` ne confère **aucun privilège ni PASS Q132**, et les plafonds de ressource déclarés ne sont pas des limites d'exécution. La future exécution devra revérifier les octets et isoler les guests malveillants. Aucun secret ni clé de signature Hub collecté.
