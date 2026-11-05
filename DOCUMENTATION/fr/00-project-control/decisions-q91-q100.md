<!-- forgepanel-doc id=FP-00-Q91-100 revision=1 status=specified -->
# Arbitrages Q91–Q100 — Versions, isolation, déploiement et migration

[English](../../en/00-project-control/decisions-q91-q100.md) · [Décisions](decisions.md) · [Q81–Q90](decisions-q81-q90.md) · [Cycle de vie](../02-architecture/website-lifecycle.md)

## Décisions explicites du propriétaire (5 novembre 2026)

Les réponses **Q91 C, Q92 D, Q93 C, Q94 D, Q95 C, Q96 D, Q97 C, Q98 C, Q99 D et Q100 D** complètent Q1–Q90. Statut **SPECIFIED**, pas IMPLEMENTED ni VERIFIED. ForgePanel reste un Core AGPL gratuit et autonome, avec Hub privé facultatif, une marque par organisation (Q55) et MFA administrateur facultatif.

| Réf. | Choix validé | Effets et limites |
|---|---|---|
| Q91 C | **Versions PHP maintenues + alertes de fin de support + migrations planifiées** | Séparer PHP du panneau et PHP client ; calendrier de maintenance, origine des paquets, compatibilité extensions et plan de migration par site. Aucun numéro de version supplémentaire n'est certifié. |
| Q92 D | **Pool PHP-FPM par site, quotas et isolation Linux renforcée selon capacité** | Identités/processus/sockets séparés, isolation des chemins, limites CPU/RAM/processus et politiques SELinux/AppArmor/cgroups disponibles ; ne jamais prétendre qu'un simple pool garantit l'isolation complète. |
| Q93 C | **Git Deploy manuel ou webhook selon politique par site, avec validation** | Identité de dépôt/ref, webhook authentifié et anti-rejeu, signatures/commits selon politique, accès restreints, staging et contrôle de santé. Un webhook n'autorise pas une commande root arbitraire. |
| Q94 D | **Staging selon politique par site : données protégées, secrets distincts, rétention et audit** | Clonage fichiers seul ou données limitées selon approbation, anonymisation/masquage, désactivation des mails/webhooks réels, domaines non indexés, délais de conservation respectés et purge contrôlée. |
| Q95 C | **Plusieurs autorités ACME + pilotes DNS-01 + alertes et renouvellement contrôlé** | Compatibilité d'autorité, preuve de domaine, certificats wildcard via challenges appropriés, secrets DNS protégés, suivi des échecs et fenêtre de renouvellement. |
| Q96 D | **Plusieurs moteurs par compte, quotas et droits séparés** | MariaDB/MySQL et PostgreSQL isolés ; Redis/Valkey facultatifs cache/queues ; quotas, rôles et secrets propres à chaque ressource. La base PostgreSQL du panneau reste distincte. |
| Q97 C | **SSH par clé, restrictions, politiques par plan, révocation, expiration et audit** | Accès uniquement aux comptes autorisés ; identité OS et périmètre limité ; pas d'élévation root ni de terminal web implicite (Q87 B). Méthode SSH certifiée/contrôles d'auth à valider. |
| Q98 C | **Webmail interchangeable, choix par serveur/fournisseur et politiques par domaine** | Fournisseur/moteur choisi parmi compatibles, DNS/TLS, isolation des boîtes, antispam et quarantaine (Q88), thèmes et autorisations dans la marque unique par organisation. |
| Q99 D | **Quotas soft/hard, alertes, délai de grâce et rallonge autorisée** | Valeurs par plan/compte/ressource, mesure effective et notifications ; dépassement temporaire décidé par un administrateur habilité, borné et audité, jamais désactivation des contraintes de sécurité/disque. |
| Q100 D | **Migration/restauration inter-serveurs avec compatibilité, staging, secrets renouvelés et reprise auditée** | Préflight OS/WebStack/PHP/DB/mail/ports, transfert chiffré et authentifié, snapshot source/cible, copie de données sous autorisation, DNS/TLS et plan de bascule/récupération. Impossible de promettre restauration universelle entre OS incompatibles. |

## Règles de configuration et responsabilités

Les réglages doivent être **administrables avec héritage** : administrateur global → serveur → organisation → plan → compte → site. Le niveau enfant ne peut pas lever une restriction parent, accéder au tenant voisin ou modifier une ressource non possédée. Les choix sont présentés uniquement si les capacités OS/driver réelles sont vérifiées. Les opérations sensibles suivent le moteur Q47 : `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → VERIFY → COMMIT/RECOVER`, avec idempotence, verrous, état observé et compensation partielle documentée.

**Core** possède la sélection PHP, l'isolation Linux, le lancement Git Deploy, le DNS-01, les moteurs de données, SSH, les quotas, le webmail, le staging et les migrations entre serveurs. **Hub** peut publier versions, recettes, compatibilité, droits premium et données commerciales, **mais ne détient aucune clé SSH/TLS privée, copie des bases/emails clients ni privilège shell**. Le Core ne requiert pas d'abonnement pour ses capacités essentielles.

## Parcours et tests obligatoires

- PHP EOL → préavis → simulation d'extensions/API → fenêtre de migration → contrôle applicatif → récupération documentée ; refus des versions dangereuses selon politique, sans suppression automatique du site.
- FPM/isolation par site : UID/GID, symlinks, sockets, limites système, processus malveillants, SELinux/AppArmor et cgroups sur chaque OS qualifié.
- Git manuel et webhook : signature, rejeu, branche non autorisée, commit modifié, disponibilité Git et erreur de build ; aucun log de token.
- Staging : consentement pour données, anonymisation, secret rotation, arrêt des mails/webhooks, nettoyage après expiration et non-divulgation.
- ACME : plusieurs autorités, comptes/challenges DNS, credentials expirés, wildcard, limites de taux et renouvellement défaillant.
- Multi-DB/Redis : séparation de comptes, ressources, connexions, quotas, backups, fail/retry et aucune exposition réseau non autorisée.
- SSH : clés expirées/révoquées, politique du plan, audit, séparation tenant, commandes et chemins autorisés.
- Webmail : moteur indisponible, domaine/fournisseur incompatibles, droits par boîte et quarantaine, protections antifraude.
- Quotas : dépassement soft, hard, grâce finie, intervention autorisée, activité concurrente et capacité disque réelle.
- Migration : changement OS/versions/profils, manque d'espace, transferts interrompus, données cohérentes, propagation DNS/TLS, secrets copiés involontairement, compensation/restore.

## Décisions à approfondir

Versions PHP encore supportées par OS et politique d'exception, méthode d'isolation privilégiée, fournisseurs/identités Git, exigences webhook et approbations, défaut d'anonymisation staging, CA ACME et pilotes DNS-01, moteurs SQL/Redis certifiés, autorité de clés SSH, moteur Webmail, durées/quotas de grâce, bande passante et délais de migration, partage source-cible et changements DNS. Aucune valeur chiffrée ni fournisseur réel n'est présumé.

**État : référence documentaire validée par le propriétaire ; implémentations HTTP, PostgreSQL, agent Go, système Linux et VM restent à tester et à construire.**
