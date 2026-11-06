<!-- forgepanel-doc id=FP-14-R3-INSTALLER revision=1 status=specified -->
# R3 — Contrat candidat d'installation sécurisée, approbations et reprise

[English](../../en/14-devops-releases/installer-lifecycle-r3.md) · [DevOps](README.md) · [IPC typé](../08-api-contracts/symfony-go-ipc-r3.md) · [QA R3](../13-tests-quality/r3-ipc-installer-gates.md)

**Statut : SPECIFIED / CANDIDATE.** Aucun installateur officiel, URL d'installation, paquet DEB/RPM ForgePanel, exécuteur privilégié, mise à jour de service ou canal Stable/Beta/Dev n'est opérationnel. Dépendances : [source Foundation v0.7 #2](https://github.com/yyogas/forgepanel/issues/2), [Symfony/PG #3](https://github.com/yyogas/forgepanel/issues/3), [Configuration Engine #9](https://github.com/yyogas/forgepanel/issues/9), [release #15](https://github.com/yyogas/forgepanel/issues/15). Owner : DevOps / Build / Release ; HANDOFF vers Security, API/IPC, Database, QA. Exigences `INST-FP-0001` à `INST-FP-0012`. **Q47, Q61 C, Q62 C, Q71/Q72, Q119/Q120 respectées sans nouvel arbitrage Q171+.**

## Chaîne de confiance — avant la première action privilégiée

**INST-FP-0001 — Provenance.** Une méthode d'installation « une commande » sera possible **uniquement après** publication d'un bootstrap vérifié avec une racine de confiance indépendante et protégée. L'URL, la version et le canal restent inconnus. L'exécutable ne doit pas considérer comme sûrs des scripts téléchargés non signés, un redirect HTTP, la sortie HTML du site officiel ou un hash servi par le même endpoint compromis. Les checksums, signatures et métadonnées signées doivent couvrir **les octets réellement installés**, pas seulement un manifest.

**INST-FP-0002 — Signature, canaux et anti-rollback.** Vérifier avant déploiement : racine de confiance, identité de l'éditeur, chaîne/rotation/révocation de clés, signature des métadonnées et de chaque artefact, digest/size exacts, canal Stable/Beta/Dev autorisé, fraîcheur/expiration et version non rétrogradée sous politique versionnée. Une erreur/rejeu/clé révoquée = `BLOCKED`. Séparer rôles de build, signature et approbation, conserver des preuves d'audit privées ; **ne jamais distribuer la clé de signature privée** au Core ni au Hub public.

**INST-FP-0003 — Qualification de la cible.** Les OS **cibles documentaires** sont Debian 12/13, Ubuntu LTS 24.04/26.04 et AlmaLinux 9/10. Cela ne prouve aucun support : vérifier séparément pour chaque OS/version/architecture la provenance des paquets, dépendances, permissions, pare-feu, AppArmor/SELinux, systemd, PHP/PG et récupération. Le **premier OS/WebStack du MVP n'est pas choisi** avant comparaison VM Q121/Q122 et veto de sécurité Q132. Les dépôts APT/DNF signés sont des contrats futurs, pas des URL publiées.

**INST-FP-0004 — Inventaire non destructif.** Inspecter réseau, listeners/ports/IP, services existants, paquets, utilisateurs/groupes, espaces, montages, OS et conflits sans changement. Distinguer serveur vierge, réinstallation et adoption de service existant. **Ne jamais écraser un service ou sa configuration non gérés** sans plan d'adoption, preuve de propriété, backup, approbation et reprise.

## Machine d'états candidate conforme au cycle Q47

| État | Entrée et preuve durable | Résultat ou refus |
|---|---|---|
| `DRAFT` | Version/OS/choix d'opérateur ; aucun effet Linux | Prépare demande |
| `PLAN` | Diff, identité de source, périmètre, rôles, dépendances, révision et hash du plan | Refuse collision de port/OS, op non déclarée |
| `PREFLIGHT` | Signatures/packages, ressources, droits, accès admin de secours, syntaxe | `BLOCKED` si confiance/accès non prouvés |
| `SNAPSHOT` | Point de récupération vérifiable, plan des secrets/DB et état antérieur | `BLOCKED` si récupération requise mais impossible |
| `STAGE` | Artefacts vérifiés en espace isolé avec quotas et hash sur octets | Aucun service actif modifié |
| `APPLY` | Autorisation récente, locks et vérification plan/signature/révision à **l'instant de l'effet** | Seules opérations Go typées explicitement autorisées |
| `VERIFY` | Contrôle services, HTTP/TLS/DB/panneau, identité et accès de secours | Pas de succès sur seul process `active` |
| `COMMIT` | État réellement observé, version/checksum, audit, réconciliation | Publication d'un résultat, pas d'une « release » automatique |
| `RECOVER` | Stoppe, identifie effets partiels, restaure uniquement étapes réversibles | Note irréversibilités, assistance manuelle contrôlée |
| `BLOCKED` | Justification et exigences non satisfaites | Aucune action privilégiée à reprendre aveuglément |

**INST-FP-0005 — Plan signé/liée à l'autorité.** L'étape `APPLY` ne peut commencer qu'avec plan de changement explicitement lié à origine/version/révision/cible/acteur/permissions, avec préconditions toujours vraies, preuve de sauvegarde et autorisation fraîche. Le format exact, les TTL/approbations et les permissions sont **ouverts à la revue** ; « mode expert » ne contourne jamais les refus.

**INST-FP-0006 — Durabilité/idempotence.** Persister intention, approbation, état et étapes réalisées avant ACK. Les redémarrages doivent comparer l'état désiré/réel avant d'appliquer une étape. Chaque étape dispose d'une identité et d'un résultat vérifiable ; une requête doublonnée ou un timeout ne peut engendrer une seconde modification cachée. **Pas de promesse de transaction atomique sur Linux et PostgreSQL ensemble.**

**INST-FP-0007 — Déploiement Linux.** Les packages et services sont gérés par des adaptateurs OS dédiés et des opérations allowlistées, avec comptes de service minimaux, permissions filesystem, unités systemd, AppArmor/SELinux et pare-feu conservés. **Aucune API `shell.exec`, commande root arbitraire, script téléchargé d'un utilisateur ou commande libre dans le manifest.** L'activation d'une génération doit conserver une voie d'administration d'urgence avant tout changement réseau.

**INST-FP-0008 — Identité et wizard.** Le bootstrap et Symfony n'ouvrent pas de compte root sur HTTP. Après admission OS, le wizard doit créer une identité d'administrateur **permanente et récupérable** avec MFA **facultative** et sessions séparées (voir [R2](../03-core/bootstrap-identity-r2.md)). Ne pas réutiliser les grants temporaires comme sessions permanentes. Le succès du plan n'est pas le succès d'activation du panneau.

**INST-FP-0009 — Sauvegarde et récupération.** Avant toute mutation sensible, vérifier snapshot/backup et accès aux clés de récupération ; préparer rollback de configuration, reprise de paquets et compensation contrôlée. Une migration SQL irréversible **ne peut pas** être défaite par un retour de code. Conserver l'état `RECOVERY_REQUIRED` et procédure manuelle documentée quand le rollback exact est impossible ; Q166 exigera plus tard la restauration isolée de chaque sauvegarde avant le label récupérable.

**INST-FP-0010 — Santé et continuité.** `VERIFY` couvre health/readiness de l'agent, PostgreSQL, UI/admin, listener/ports, logs de diagnostic expurgés, TLS et parcours de connexion ; pour changement réseau, contrôle positif de l'ancien/nouveau chemin administrateur jusqu'à validation, ou refus. Les métriques/signes de vie ne certifient pas un service pleinement opérationnel.

**INST-FP-0011 — Observabilité / CI.** Tracer sans secrets : commit, version, OS/arch, image VM, checksum de signature, résultat de trust, digest du plan, acteur et approbation, chaque étape, corrélation, droits/locks, résultat de health et compensation. Conserver rapports `PASS/FAIL/BLOCKED/SKIP` exacts par environnement ; une CI documentaire verte, des fixtures ou un conteneur ne certifient **jamais** systemd/paquets/isolement d'une VM réelle. Q152/Q162 futurs exigent preuves signées et stockage immuable privé.

**INST-FP-0012 — Compatibilité/évolution.** Installation vierge, relance, upgrade, patch, rollback, retrait/désinstallation et récupération d'échec ont des parcours documentés et **tests négatifs**. Migrations DB avant/après upgrade selon politique, sans downgrade prétendument automatique. Hub facultatif ne devient ni contrôleur root ni prérequis pour mise en service/récupération du Core libre. Aucun passage `stable/main/production` sans gates et revue nécessaires.

## Refus, récupération et responsabilités

| Condition | Attitude imposée |
|---|---|
| Signature invalide, trust root inconnue/révoquée, manifeste altéré, version stale | `BLOCKED` avant étape privilégiée, événement d'audit expurgé |
| OS/paquet/service non supporté ou plugin non fiable | Refuser, ne pas supposer qu'un autre OS/profil fonctionne |
| Fichier préexistant non géré, port occupé, droit tenant insuffisant | Refuser ou présenter un plan explicite d'adoption/compensation |
| Disque plein, coupure réseau, reboot, service cassé après `APPLY` | Restaurer uniquement ce qui est sûr et prouvé, sinon `RECOVERY_REQUIRED` |
| SQL DDL irréversible ou clé de backup inaccessible | Ne pas promettre « rollback complet » ou « récupérable » |
| Hub indisponible ou refus de télémétrie | Le Core libre continue sans commande externe |

## Revues ouvertes et preuves de sortie

- **API/IPC :** toute étape Go privilégiée doit correspondre à une entrée du [registre candidat](../../evidence/typed-agent-operations-v1.json), puis à un contrat approuvé versionné, sans commande libre.
- **Database :** migrations, jobs et backups nécessitent schémas approuvés ; aucune table/colonne n'est définie ici.
- **Security :** preuve opérateur, séparation des rôles/approbations, signature, secret store, délais, récupération locale ; audit indépendant toujours absent.
- **QA / DevOps :** exécuter [`R3-INSTALL-TEST-001..012`](../13-tests-quality/r3-ipc-installer-gates.md) dans une VM jetable et documenter OS/commit exacts, pannes et reprise.

**`DOC-GAP-005` reste OPEN.** Ce contrat n'autorise aucune installation ; le vrai code Foundation, R2 Symfony/PostgreSQL et l'exécuteur Linux n'existent pas encore comme produit intégré.
