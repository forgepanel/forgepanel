<!-- forgepanel-doc id=FP-12-FOUNDATION-RECOVERY revision=1 status=documented -->
# R1 — Récupération des sources Foundation originales (7 novembre 2026)

[English](../../en/12-development/foundation-source-recovery.md) · [Registre initial des sources](../../evidence/sources.json) · [Manifeste de récupération](../../evidence/foundation-recovery-2026-11-07.json) · [Contrat de précontrôle](source-archive-intake.md)

## Archives effectivement récupérées

Les fichiers historiques produits pour le propriétaire ont été retrouvés dans sa **bibliothèque ChatGPT privée**, puis copiés dans un dossier de récupération privé accessible au propriétaire ; ils n'ont **pas** été publiés dans ce dépôt Git public. L'archive originale `SRC-03` (`ForgePanel_Foundation_v0.7_source.zip`) contient 92 fichiers réguliers et possède l'empreinte SHA-256 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`, identique à celle du registre canonique antérieur. Le contrôle CRC ZIP et le contrôle des chemins de l'archive ont réussi. L'archive indépendante `v0.7.1_optional_MFA` contient 93 fichiers et a pour SHA-256 `83fe6e77713f68d69595e74864aa1c33f75d88b6ba4199e03d5ef30a7060402c` ; l'historique `v0.6` contient 14 fichiers et a pour SHA-256 `8f800471ab4c2823ae6151ac478fe821cf26f5718e1449ad8f02ab0d430983b0`. Ces contrôles attestent l'identité des octets et la validité ZIP, pas l'authenticité d'un éditeur, la licence ou la sûreté en production.

## Contrôles réellement exécutés sur les sources récupérées

Le 07/11/2026, les ZIP authentiques v0.7 et v0.7.1 ont été extraits dans des répertoires temporaires isolés puis `bash scripts/check.sh` a retourné **0** sur les deux, sous un compte Linux **non-root** et avec dépendances Go hors ligne (`GOTOOLCHAIN=local`, `GOPROXY=off`, `GOSUMDB=off`). Le script fourni exécute les tests Go et détecteur de concurrence/vet, la syntaxe PHP et les tests métier PHP autonomes, compile la CLI Go et génère un plan d'installation **non exécutable**. Environnement : Go 1.23.2 et PHP 8.4.24. Le plan indique explicitement `executable=false`, `production_apply_not_implemented`, `signed_release_channel_not_configured` et `os_package_manifests_not_certified`.

**Non exécutés / non vérifiés :** HTTP Symfony réel, PostgreSQL/transactions/concurrence, isolation inter-tenant sur hôte système, qualification OS/VM, installation exécutable, restauration, audit de sécurité offensif, provenance tierce, analyse juridique complète et signature de release. La réussite des tests autonomes n'est pas la certification d'une version exploitable.

## Sécurité et limites de publication

Les deux archives v0.7 et v0.7.1 contiennent le chemin `apps/panel/.env`. Cette présence **ne prouve pas qu'un secret actif soit présent**, mais le fichier ne doit jamais être commité dans Git public sans audit spécifique des secrets et de la provenance. Les originaux inchangés sont conservés dans le dossier privé ; un candidat séparé exclut `.env`, les résultats de tests générés et certains éléments historiques. Le dépôt Core est actuellement **public** ; les textes AGPL/commerciaux/CLA exacts et les droits de distribution tiers restent ouverts. Tout import de code public exige donc un contrôle explicite sécurité/publication/juridique. **Ne pas transférer du code Core dans le Hub privé pour contourner ce garde-fou.**

## État R1 et handoff

**SOURCES RETROUVÉES / SHA EXACT CONFIRMÉ / TESTS NATIFS HORS LIGNE RÉUSSIS / NON IMPORTÉ DANS GIT.** L'ordre approuvé reste R1 import → R2 Symfony/PostgreSQL réel → R3 installateur/VM qualifiés → R4 site PHP/HTTPS → R5 ABI neutre d'extensions → R6 Hub privé facultatif. R1 doit encore contrôler sources et droits, vérifier l'import assaini par empreintes individuelles, obtenir les autorisations de publication/visibilité, ouvrir une PR `features/*`, exécuter les tests sur ce commit, réaliser les revues puis intégrer. Voir [l'issue d'import #2](https://github.com/yyogas/forgepanel/issues/2). Les anciens documents disant que le ZIP est indisponible sont désormais dépassés **uniquement sur ce point factuel** ; leurs avertissements de sécurité et de réalisation demeurent.