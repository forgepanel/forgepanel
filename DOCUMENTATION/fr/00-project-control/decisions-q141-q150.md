<!-- forgepanel-doc id=FP-00-Q141-150 revision=1 status=specified -->
# Arbitrages Q141–Q150 — Qualification technique, récupération et publication sécurisée

[English](../../en/00-project-control/decisions-q141-q150.md) · [Q131–Q140](decisions-q131-q140.md) · [Qualification MVP](mvp-qualification.md) · [Exigences détaillées](../02-architecture/certification-backup-security.md)

## Choix confirmés par le propriétaire — 5 novembre 2026

**Q141 D, Q142 D, Q143 C, Q144 D, Q145 D, Q146 C, Q147 C, Q148 C, Q149 C, Q150 D** sont retenus. Ils **complètent Q1–Q140** sans révoquer les arbitrages de sécurité, de licence, de Hub optionnel ou de première livraison. **État : SPECIFIED, non IMPLEMENTED/VERIFIED.** Aucune VM, sauvegarde, bêta, preuve cryptographique ou publication de sécurité ne devient opérationnelle par cette documentation.

| ID | Choix du propriétaire | Contrat de mise en œuvre et sécurité |
|---|---|---|
| Q141 D | **Pilotes VM locales et cloud + runners CI compatibles + rapports communs** | Contrat de test indépendant du fournisseur pour QEMU/KVM ou VM cloud autorisées, VM complètes avec snapshots et pannes simulées ; rapport normalisé OS/version/architecture/WebStack/commit, PASS/FAIL/SKIP, artefacts et restauration. Le CI ne certifie pas un OS sans exécution VM réelle. |
| Q142 D | **Budgets de performance par type d'application + détection des régressions entre versions** | Références de test pour PHP simple, CMS et autres applications retenues ; débit, latence percentile, erreurs, CPU/RAM et reprise. Budgets configurables et comparaisons à environnement contrôlé. **Critères éliminatoires de sécurité et récupération Q132 prioritaires**, même si les benchmarks sont bons. Aucun seuil numérique décidé. |
| Q143 C | **Proposer les enregistrements DNS + revérifier A/AAAA, ports et certificat** | Assistant diagnostic pour DNS **externe**, port 80 et challenge ACME HTTP-01, port 443 et certificat valide. Générer les instructions/valeurs attendues, puis retester après intervention autorisée. **Aucune écriture automatique chez un fournisseur DNS** n'est choisie par Q143 C. |
| Q144 D | **Politiques de mises à jour OS par serveur**, avec diffusion progressive multi-serveurs **ultérieure** | Par serveur : canaux/paquets autorisés, maintenance, plan d'impact, backup, approbation, reboot, santé/reprise, audit et version de politique. La coordination multi-serveurs suivra Q67/Q77 une fois l'agent et HA vérifiés ; elle ne bloque pas le MVP mono-serveur. |
| Q145 D | **Coffre de secrets et copie de récupération sécurisée + KMS externe facultatif et plusieurs autorités de récupération** | Chiffrement des backups locaux Q135 et gestion des clés : séparation clés/données, accès et rotation, restauration hors serveur, mécanisme de plusieurs gardiens/approbateurs lorsque choisi. **KMS externe non obligatoire**, Core récupérable hors Hub. Ne pas supposer que chiffrement local et clé stockée sur le même disque suffisent après panne. |
| Q146 C | **SFTP par identité/chemin isolés, sans shell, avec expiration/révocation, quotas et audit** | Compte autorisé Q136 : clés, racine/chemins canoniques, interdiction de traversée/symlink inter-tenants, quotas et traces ; suspendre/expirer l'accès sans effacer les fichiers. Pas de terminal web ni de compte root. |
| Q147 C | **Bêta : pause si incidents critiques, health checks/seuils configurables et récupération** | Vagues autorisées Q137, critères de défaillance par version/cohorte, seuils de santé, suspension de nouvelles installations/mises à jour, notification et stratégie de récupération. Les informations remontées des testeurs restent opt-in ou contractuellement bornées (Q6) ; aucune collecte forcée. |
| Q148 C | **Paire de clés locale, challenge signé, rotation/anti-rejeu, preuve d'organisation et secours manuel** | Identité d'installation premium Q128/Q138 côté Hub avec challenge horodaté, nonce, liaison à l'organisation et au serveur cible, contrôles de rotation/révocation et procédure de serveur perdu. La **seconde validation selon risque Q138 D demeure**. Ne pas demander de secret root ni prétendre que la clé seule empêche une copie complète. |
| Q149 C | **Délais partenaires par gravité et contrat, escalade, alertes et retrait** | Q114/Q129/Q139 restent : revue humaine de chaque version et obligations de maintenance/sécurité ; niveaux de sévérité, échéances contractuelles, rappel, escalade, mesures de retrait et avis client. **Aucun délai chiffré ou SLA implicite.** |
| Q150 D | **Avis de sécurité signés et historiques, notifications configurables, coordination partenaires et calendrier de divulgation selon le risque** | Responsable/suppléant Q130 et triage Q140 ; avis versionnés et authentifiés, périmètre touché, remédiation et divulgation coordonnée, pas de date universelle, pas de publication de vulnérabilités non corrigées par automatisme. Diffusion d'avis sans télémétrie obligatoire ni pouvoir de coupure du Core. |

## Impacts sur la première version et sur Q120

Le **MVP Q119 B/R4** demeure installateur/CLI/wizard/identité PostgreSQL + site PHP/domaine **DNS externe/ACME HTTP-01** + HTTPS, gestionnaire de site, opérations VPS contrôlées, backup chiffré local et restauration réelle. Q141/Q142 renforcent la preuve VM/performances avant le choix du premier OS/WebStack (Q121/Q122), Q143 précise l'assistant DNS sans écriture automatique, Q144 la politique serveur et Q145 la **récupérabilité des clés de backup** ; Q146 ajoute des refus et audits SFTP. **Aucun KMS cloud ni cluster de mises à jour n'est un prérequis obligatoire à R4.**

**Après MVP** : Q147 raffine la bêta privée interne→vagues, avec pause/récupération et télémétrie consentie. **Après l'ABI générique R5**, Hub R6 pourra développer Q148–Q150 : identité cryptographique de transfert, conformité partenaires et avis signés/coordinés ; les utilisateurs du Core gratuit ne doivent pas dépendre du Hub pour leur serveur.

## Tests attendus et garde-fous

- VM locales/cloud : vraie isolation système, snapshots restaurés, panne d'installation réseau/disque, rapports identiques pour chaque pilote, skips explicites.
- Perf : workloads/version/OS/ressources fixés ; régression statistiquement interprétable, aucune optimisation autorisée si sécurité violée.
- DNS : mauvais A/AAAA, IPv6, port 80 filtré, challenge HTTP-01 mal routé, contrôle du certificat puis retest après correction **manuelle**.
- OS : mise à jour interrompue, reboot, version de politique obsolète, backup inrestaurable, serveur voisin jamais affecté.
- Secrets/backups : perte du disque et du coffre, clé absente, erreur d'approbation multi-gardiens, KMS externe inaccessible ; procédure locale de récupération indépendante.
- SFTP : utilisateur expiré, clé révoquée, mauvais chemin, lien symbolique, quota atteint, refus inter-organisations, journaux expurgés.
- Bêta : incident critique déclenchant pause de vague, récupération vérifiée, pas de suppression de données ni de droits logiciels acquis.
- Hub : nonce rejoué/clé volée/org erronée/transfert simultané/serveur détruit, partenaires hors délai, avis signé invalide et divulgation non autorisée.

[Contrats de certification et récupération](../02-architecture/certification-backup-security.md) · [Roadmap](implementation-roadmap.md).

## Restent à choisir

Fournisseur CI/cloud et coût, profils de workloads et seuils de budgets, valeurs DNS suggérées par l'adresse réelle du site, règles de maintenance par défaut, coffre/KMS/technique de partage de récupération, durées des accès SFTP, seuils de suspension bêta, format des défis de possession, délais contractuels partenaires et politique exacte de divulgation. **Aucun fournisseur, délai, nombre de gardiens ou seuil n'est présélectionné.**
