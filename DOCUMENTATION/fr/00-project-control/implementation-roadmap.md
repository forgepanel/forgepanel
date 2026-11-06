<!-- forgepanel-doc id=FP-00-EXECUTION revision=16 status=specified -->
# Roadmap technique de réalisation — décision Q120 D et MVP Q119 B

[English](../../en/00-project-control/implementation-roadmap.md) · [État officiel](status.md) · [Décisions Q111–Q120](decisions-q111-q120.md)

## Ordre approuvé du propriétaire

**Importer les sources → vérifier Symfony/PostgreSQL → construire et tester l'installateur → exploiter le premier site PHP/VPS → valider une API d'extension générique → développer/intégrer ForgePanel-Hub.**

Cette séquence **remplace les priorités implicites** qui laisseraient les modules premium/marketplace précéder un Core fonctionnel ; elle ne supprime pas les décisions Q1–Q110. Les étapes peuvent comporter des branches préparatoires en parallèle, mais **aucune phase dépendante ne peut être déclarée achevée avant la preuve de la précédente**. Toutes les étapes ci-dessous restent à exécuter ; les contrôles documentaires ne prouvent pas leur réalisation.

| Gate | Travail concret | Sortie vérifiable et conditions de refus |
|---|---|---|
| **R1 — Sources** | Import de l'archive Foundation v0.7 vérifiée, examen des différences avec le correctif MFA facultatif v0.7.1, provenance/hashes, licence marquée en attente | PR `features/* → develop`, structure Go/PHP importée sans secrets ni binaires générés, `make check`/Go race/vet/PHP et refus de `install apply` tant qu'il n'est pas sécurisé. Préserver la documentation bilingue et le changelog unique. Suivi : [issue #2](https://github.com/yyogas/forgepanel/issues/2), [MFA #6](https://github.com/yyogas/forgepanel/issues/6). |
| **R2 — Symfony/PostgreSQL** | Dépendances Composer résolues/verrouillées, runtime Symfony actif, connexion PDO/PG dédiée, setup initial et identité permanente ; option activer/ignorer MFA, CSRF/HTTPS/sessions | Tests HTTP et navigateur du wizard, accès admin, CSRF, origine, autorisation, MFA facultatif, reprise et PostgreSQL réels (rollback, concurrence, redémarrage, réponse perdue). Reproduire sur revision précise. Suivi : [issue #3](https://github.com/yyogas/forgepanel/issues/3). |
| **R3 — Installateur sûr** | Build Go, provenance/signatures, commande vérifiée, préflight, étapes idempotentes, systemd/logs/reprise. **Comparer les prérequis et essais VM des OS cibles avant de choisir le premier OS (Q121 D).** | Preuves comparatives install/upgrade/échecs/récupération, OS/version/commit ; **aucun OS prédéterminé** et aucune certification des six OS sans test distinct. [Qualification](mvp-qualification.md) · [issue #15](https://github.com/yyogas/forgepanel/issues/15). |
| **R4 — Site PHP et VPS minimum** | **Choisir la première WebStack après essais compatibilité/sécurité (Q122 D)** ; site PHP isolé avec domaine géré par **DNS externe**, ACME **HTTP-01** et HTTPS automatique (Q123 A) ; identité permanente et **rôles admin/gestionnaire de site : PHP/domaines/TLS/fichiers/SFTP et backup/restore bornés par RBAC** (Q124 B/Q136 C) ; surveillance VPS, logs, **opérations de paquets/mises à jour OS contrôlées** (Q125 B) ; **backup/restauration testés configuration du panneau + fichiers PHP** (Q126 B). | VM propre : install/wizard/login → site PHP/domaine/DNS externe → challenge HTTP sur port 80 → HTTPS réel → accès SFTP au site autorisé et refus inter-tenant → permissions refusées → paquet mis à jour avec plan/audit → backup et restauration réels. Le stockage PG indispensable au panneau exige une reprise cohérente. Aucune WebStack ni CA choisie d'avance. [Qualification](mvp-qualification.md) · [site #20](https://github.com/yyogas/forgepanel/issues/20) · [MVP #29](https://github.com/yyogas/forgepanel/issues/29). |
| **R5 — API neutre d'extension** | ABI versionnée pour services détachés, permission fine, cycle verify/stage/activate/disable/remove et plugin d'essai **non Hub** | Extension neutre signée fonctionne sur Core normal, est refusée si non fiable/incompatible, et son arrêt/suppression ne stoppe jamais les sites. Tests permissions/versions/rollback. Suivi : [issue #7](https://github.com/yyogas/forgepanel/issues/7). |
| **R6 — Hub après R5** | Symfony Hub isolé + PostgreSQL distinct, organisations, offres, paiement sandbox, licence/pools, catalogue officiel/partenaires, vérification des droits et distribution signée | Tests interopérabilité Core-Hub, client offline, webhooks signés/idempotents, transferts de licences, motif de révocation, confidentialité ; aucune nécessité du Hub pour la connexion ou la réparation du Core. Suivi : [dépôt Hub](https://github.com/yyogas/forgepanel-hub) et ses issues. |

**R4 est le périmètre de première version fonctionnelle Q119 B**. Les opérations R5/R6 sont **postérieures** à ce jalon. La cible Q54 reste hébergement mutualisé + administration VPS ; ne pas exiger cluster HA, Webmail, DNS local ou tous les langages avant la première démonstration. Le choix du **premier OS, WebStack et domaine de test** doit être étayé, non présumé ici.

## Extension Q121–Q130 : preuves MVP, bêta et responsabilités

**Q121 D / Q122 D :** sélectionner le premier couple OS/WebStack **uniquement à partir de comparatifs VM** ; aucune plateforme ni pile choisie par l'utilisateur. **Q123 A :** parcours v1 fondé sur DNS **externe** et validation ACME **HTTP-01**, sans exiger DNS natif ou DNS-01 au premier jalon. **Q124 B / Q125 B / Q126 B :** compte administrateur et gestionnaire de site, VPS supervisé avec gestion contrôlée des paquets, sauvegarde de config panneau et fichiers PHP avec restauration **réellement testée**. La [matrice de qualification](mvp-qualification.md) décrit les cas négatifs.

**Q127 B :** après tests internes isolés, une **bêta privée** limitée à des testeurs autorisés est possible seulement avec validation du propriétaire, canal sécurité opérationnel et conditions de licence/diffusion vérifiées **aussi pour ces destinataires externes** ; ce n'est pas une release publique ni un passe-droit juridique. Les Q128 D (licences transférables et récupération manuelle de serveur perdu), Q129 C (maintenance partenaires contractualisée/alertes/retrait) attendent le **Hub après ABI**. **Q130 C** demande un responsable sécurité et un suppléant **effectivement désignés**, triage et notifications coordonnées ; ne pas inventer leur identité ou un email.

## Précisions Q131–Q140 — critères de sortie

- **R3, Q131 D** : comparer la matrice VM **locales + CI**, snapshots, pannes simulées, rapports OS/versions avec résultats `PASS/FAIL/SKIP`; **aucun OS présélectionné**. **Q132 D** ajoute aux profils WebStack des tests de charge, maintenance et récupération avec **critères éliminatoires sécurité** indépendants des performances.
- **R4, Q133 C** : assistant de diagnostic **A/AAAA**, port **80**, route HTTP-01 puis disponibilité **HTTPS** ; DNS externe retenu (Q123). **Q134 C** : mises à jour OS avec plan d'impact, backup, santé et récupération. **Q135 B** : sauvegarde **locale chiffrée**, remote **facultatif**, et vraie restauration de configuration panneau et fichiers PHP. **Q136 C** : rôle gestionnaire de site avec PHP/domaines/TLS/fichiers/**SFTP/backup/restore**, dans les politiques et quotas, sans privilèges OS.
- **Après R4, Q137 D** : bêta privée sur invitations et conditions acceptées, **vagues progressives**, canal bugs/versions, **pause/suspension et procédure de récupération** ; aucun déploiement bêta avant les preuves VM, la vérification juridique des destinataires et le triage sécurité.
- **Après R5/Hub, Q138 D** : transferts commerciaux avec preuve cryptographique, anti-abus, **deuxième validation configurable** lors de la récupération risquée d'un serveur perdu. **Q139 C** : partenaires sous contrats Q129 avec gravité, alertes, escalade et retrait. **Q140 C** : responsable + suppléant Q130 et communication coordonnée des correctifs/avis ; canaux Q118 vérifiés.

Les choix Q131–Q140 n'autorisent ni défaut d'OS/WebStack, ni bêta ouverte, ni suppression des données lors de la suspension d'un accès. [Matrice de qualification mise à jour](mvp-qualification.md) · [Décisions](decisions-q131-q140.md). **Tout est encore à réaliser et à vérifier.**

## Précisions Q141–Q150 — preuves et frontières

- **R3, Q141 D** : pilotes VM **local/cloud**, runners CI compatibles, snapshots/injection de pannes et rapports de certification OS/stack/commit structurés identiquement ; ne pas qualifier les VM avec des fixtures ou des jobs `SKIP`. **Q142 D** : classer les applications et définir budgets de performance configurables, comparer les régressions entre versions et appliquer les veto de sécurité Q132 avant tout score.
- **R4, Q143 C** : proposer **les enregistrements DNS externes** du site et permettre revérification A/AAAA/80/HTTP-01/443/TLS **sans correction automatique DNS**. **Q144 D** : politiques de mise à jour OS **par serveur** avec plan/backup/santé/reprise, orchestration multi-serveurs ultérieure. **Q145 D** : backups chiffrés locaux + clés de récupération accessibles après perte du serveur, coffre, copie de secours protégée, KMS externe et récupération multi-autorité **facultatifs**. **Q146 C** : SFTP réel sans shell, expiration/révocation, quotas et audit, refus de traversée et d'accès inter-tenants.
- **Après R4, Q147 C** : cohortes de bêta Q137, **contrôles de santé et seuils configurables**, arrêt des nouvelles vagues sur incident grave, notification et récupération, sans télémétrie obligatoire du Core gratuit ni destruction de données/droits.
- **R6 Hub après R5, Q148 C** : clés d'identité installation, challenge signé, rotation/anti-rejeu, contrôle organisation et secours manuel serveur perdu, avec approbation additionnelle **selon risque Q138**. **Q149 C** : sévérité et délais **contractuels** partenaires, alertes/escalade/retrait. **Q150 D** : avis signés et historisés, notifications configurables, coordination partenaire et **calendrier de divulgation selon le risque**, sans SLA ni délai inventés.

**Le premier OS/WebStack reste à choisir par preuves Q121/Q122 ; aucun composant de cette liste n'est déclaré opérationnel.** [Décisions Q141–Q150](decisions-q141-q150.md) · [Matrice MVP](mvp-qualification.md).

## Q151–Q160 — ordre des pilotes et preuves de validation

**R3 (qualification)** : commencer **QEMU/KVM local (Q151 A)**, conserver l'interface multi-pilotes pour le cloud plus tard. Attacher à chaque qualification une **matrice interne**, un rapport **signé et historisé** avec provenance, snapshots et résultats individuels **PASS/FAIL/SKIP (Q152 C)**. Les budgets de performance par type d'application bloquent selon gravité ; une exception **approuvée et auditée** peut concerner une régression de performances, **jamais les critères éliminatoires de sécurité/récupération Q132** (Q153 C).

**R4 (premier site)** : DNS externe **A/AAAA vérifié seulement s'il est publié**, chaque famille présente devant rendre HTTP-01/HTTPS possible (Q154 C), assistant Q143 propose les valeurs et **revérifie sans modifier les DNS**. Mises à jour/reboot OS **par serveur**, après approbation/backup/health/récupération (Q155 C). Backup chiffré local **non déclaré récupérable** tant que l'accès à une clé de secours n'a pas été vérifié périodiquement et qu'une **restauration isolée réelle** n'a pas réussi (Q156 C) ; KMS externe et gardiens multiples facultatifs Q145. Accès SFTP **sans shell**, clés publiques **gérées sous politique site**, expirables/révocables, quotas/audit et validation sensible (Q157 C).

**Après R4 (bêta privée)** : santé **locale**, remontées manuelles et diagnostics minimisés **avec opt-ins distincts** par cohorte (Q158 C). Les seuils d'arrêt et la récupération Q147 s'appliquent sans télémétrie imposée. **Hub R6 après ABI R5** : Q159 C déclenche l'analyse antifraude des transferts serveur perdu/répété/org incohérente/compromission en conservant la seconde approbation selon risque Q138 ; Q160 C prévoit avis signés **FR/EN et structurés pour machine** avec notification configurable et divulgation coordonnée Q150.

La stratégie Q120 D reste **sources → Symfony/PG → installateur → premier site/VPS → ABI neutre → Hub**, sans calendrier ni statut d'implémentation présumé. [Décisions Q151–Q160](decisions-q151-q160.md).

## Contrôles transversaux et diffusion publique

Avant de déclarer une release utilisable : chaque environnement testé est nommé (OS/version, composants, commit, outils, statut), la sécurité de la connexion et du wizard est prouvée, les sauvegardes/restaurations réelles passent, et les défaillances sont consignées. Une CI documentaire ou des tests de domaine PHP ne remplacent pas HTTP, PostgreSQL et VM.

Avant **distribution publique** : conclure la revue juridique AGPL/commercial (Q111) et CLA électronique (Q112), droits des dépendances et politique de marque ; configurer et **vérifier** signalement privé GitHub + contact email sécurité (Q118) et procédures de triage. Ne pas inventer d'adresse, ne pas choisir de licence finale sans décision juridique. Les deux canaux de sécurité ne sont pas considérés ouverts avant vérification.

À chaque étape : branch `features/*`, PR ciblée vers `develop`, tests et preuves, revue quand disponible, mise à jour FR/EN et changelog ; promotions contrôlées ultérieurement vers `stable`, `main`, `production`, **jamais automatiques** sur une décision de documentation.

## Risques et dépendances

Le code Core n'est **pas encore importé** dans `develop` ; le prototype v0.7.1 MFA facultatif reste en archive séparée. Les intégrations Symfony/PG et l'installateur ne sont pas démontrés par les workflows actuels. Le plan ne promet pas de calendrier ou d'effet système immédiat. Toute revendication de progression doit être attachée à un commit, un test et un environnement vérifiables.

## Preuves de sortie additionnelles Q151–Q160

[Tests MVP par gate R3/R4/R5/R6](../13-tests-quality/mvp-gates-q151-q160.md) : les conditions de sortie sont des scénarios positifs **et négatifs**. KVM/rapports signés/budgets Q153 en R3 ; DNS sur IP publiées, reboot par serveur, **clés accessibles + restauration isolée réelle** et SFTP public-key limité en R4 ; bêta à consentement/cohortes ensuite ; Hub antifraude/avis signés et structurés après ABI R5. **PLANNED : aucune VM ni sauvegarde testée par les contrôles documentaires.**

## Complément de roadmap Q161–Q170 — sorties réelles

**R3** : runner local KVM éphémère avec images/quotas/nettoyage (Q161 C), rapports **internes signés** en stockage privé immuable (Q162 B), exceptions **performance** fondées sur gravité, séparation des approbateurs, expiration et audit sans toucher aux veto Q132 (Q163 C). **R4** : DNS/HTTP-01 vérifié localement **et** depuis une sonde externe indépendante sur chaque A/AAAA publié (Q164 B) ; actions non destructives de récupération OS bornées avec approbation des risques (Q165 C) ; chaque backup restauré isolément avant statut récupérable, tests profonds périodiques et exercices perte hôte/clé selon criticité (Q166 C) ; clés **publiques** SFTP sous politique d'algorithmes/rotation/approbations (Q167 C). **Bêta après R4** : consentements distincts et cohortes anti-réidentification (Q168 C). **Hub R6 après ABI R5** : règles versionnées antifraude transferts (Q169 C) et avis signés JSON Schema FR/EN (Q170 B). [Matrice de tests](../13-tests-quality/mvp-gates-q161-q170.md). Aucun des tests VM/récupération n'est encore exécuté.

## Porte R1 — vérification et quarantaine des sources sans import

La chaîne outillée R1 possède désormais `verify_source_archive.py` (préflight en lecture seule) et `stage_source_archive.py` (**prévisualisation par défaut**, puis copie explicite non-root, répertoire privé neuf et hash de chaque fichier). Cette préparation n'exécute pas le PHP/Go historique, n'ajoute aucun fichier Core au dépôt, ne valide ni licence ni installation ; elle précède la revue humaine et la PR d'import des sources originales. L'archive SRC-03 demeure indisponible : **import R1 bloqué, R2–R6 inchangés**. [Contrat de quarantaine](../12-development/source-staging.md).

## Critère d'entrée R1 supplémentaire : audit des fichiers copiés

L'issue #2 (import du vrai code Foundation) exige désormais la séquence explicite : archive SRC-03 originale → [préflight](../12-development/source-archive-intake.md) → [copie privée](../12-development/source-staging.md) → [comparaison ZIP/reçu/disque](../12-development/source-staging-audit.md) → revue licence/sécurité → import en PR distincte avec **re-hash des octets à l'import** → tests PHP/Go. Les utilitaires de préflight et audit ne sont **pas** l'implémentation du panneau, et le vrai ZIP n'est pas disponible dans ce contexte.

## Préparation parallèle R3 — inspection KVM distincte du pilote de VM

Sans modifier l'ordre approuvé **R1 → R2 → R3 → R4 → R5 → R6**, l'utilitaire Go isolé [`tools/kvm-host-probe`](../14-devops-releases/kvm-host-probe.md) prépare **uniquement une observation non privilégiée** de l'hôte local (Q151 A/Q161 C). Il ne devient pas le pilote QEMU/KVM, ne choisit pas d'OS, ne produit ni images épinglées/quotas/snapshots ni rapport signé et ne remplace aucune preuve d'installation ou de restauration. Ses tests unitaires sont indépendants de l'import Foundation original encore bloqué en R1.

## Préparation parallèle R3 — admission d'image, pas exécution VM

Après la sonde hôte, [admission QCOW2](../14-devops-releases/kvm-image-admission.md) vérifie le manifest, l'empreinte du fichier et les limites **expressément fournies**, sans valeur par défaut, opération système ou QEMU. Les futures étapes restent : provenance d'image signée/autorisation → copie immuable et attestation de l'image utilisée → VM éphémère KVM isolée/quotas effectifs → snapshots, échec/reprise → rapports signés Q152 et stockage immuable privé Q162 → qualification R3 avec veto Q132. **R1 → R2 → R3 → R4 → R5 → R6 inchangé** ; les sources Foundation restent manquantes.

## Préparation R3 — fixation provisoire des octets d’image

La [copie privée vérifiée](../14-devops-releases/kvm-image-staging.md) complète la sonde et l’admission R3 sans changer **R1 → R2 → R3 → R4 → R5 → R6**. Elle génère `image.qcow2` et un reçu de provenance non signé dans un dossier de laboratoire privé ; le futur runner devra **revérifier au moment du lancement** les octets, prouver l'isolement, appliquer les quotas et nettoyer automatiquement ses ressources, avant toute preuve Q152/Q162. R1 Foundation v0.7 demeure bloqué par le ZIP historique manquant.

## Lot documentaire R3 — prérequis IPC et installateur avant toute implémentation

[R3 IPC typé](../08-api-contracts/symfony-go-ipc-r3.md), [plan d'installation/reprise](../14-devops-releases/installer-lifecycle-r3.md) et [QA planifiée](../13-tests-quality/r3-ipc-installer-gates.md) normalisent l'ordre de validation, sans passer outre R1 → R2. Après import SRC-03 et Symfony/PostgreSQL testés : valider contrats/permissions/IPC, modèle durable des jobs et migrations, sécurité du daemon/OS, source et signature des artefacts ; ensuite seulement implanter l'installateur et exécuter les VM jetables. Les choix de transport, seuils, fournisseurs et OS pilote sont encore ouverts. **`DOC-GAP-005` et `DOC-GAP-006` ne sont pas fermés**.

## Ordre de validation documentaire R2/R3 : état durable et identité du pair

Avant toute opération système, ratifier le [modèle job/idempotence/fencing](../09-database/durable-jobs-r3.md) via Database et le [protocole de confiance du pair](../08-api-contracts/local-peer-trust-r3.md) via Security/API. R1 source importée et R2 Symfony/PG démontrés restent des dépendances strictes de R3. Développer ensuite jobs/bridge **sans commande shell privilégiée générique**, vérifier séparément authz, perte d'ACK, vieux worker, failover et impact SQL/Linux sur VM ; promouvoir seulement après QA/révision. [24 cas prévus](../13-tests-quality/r3-jobs-peer-gates.md), aucun exécuté.

## Prochain gate R3 — ratification avant migrations et comptes Linux

Les trois [contrats physiques DB](../09-database/physical-jobs-model-r3.md), [comptes Linux](../14-devops-releases/linux-service-identities-r3.md) et [effets par action](../08-api-contracts/typed-execution-recovery-r3.md) **n'autorisent pas** leur application. Ordre recommandé : récupérer SRC-03 → prouver Symfony/PG R2 → revue Database des tables/transactions/RLS → revue Security/DevOps des UID/socket/systemd/LSM → revue API/IPC des handlers/fencing/recovery → écrire migrations/handlers sur PR distinctes → campagnes SQL/VM réelles avec preuves par commit → envisager le premier OS/stack après veto Q132. R1→R2→R3→R4→R5→R6 demeure inchangé ; 36 tests de référence PLANNED.
