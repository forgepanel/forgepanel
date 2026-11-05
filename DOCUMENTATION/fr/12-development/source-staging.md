<!-- forgepanel-doc id=FP-12-SOURCE-STAGING revision=1 status=documented -->
# Mise en quarantaine contrôlée des sources — R1

[English](../../en/12-development/source-staging.md) · [Préflight](source-archive-intake.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Risques](../19-audits-risks/README.md)

## Objet et statut

**Outil Python implémenté :** \`scripts/stage_source_archive.py\` prépare une copie des **fichiers réguliers** d'une archive ZIP déjà vérifiée dans un répertoire privé et entièrement nouveau. **Le mode par défaut n'écrit rien.** Il ne s'agit ni d'un installateur, ni d'un import Git, ni d'un chargeur d'extensions.

L'archive de référence \`ForgePanel_Foundation_v0.7_source.zip\` reste indisponible ici. Le contrôle s'appuie sur le registre canonique [SRC-03](../../evidence/sources.json) : 92 fichiers, SHA-256 \`19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a\`. **Aucune source applicative PHP/Go n'a été importée ni exécutée.**

## Deux commandes distinctes

\`\`\`bash
# Mode prévisualisation, lecture seule : pas de création du dossier.
python3 scripts/stage_source_archive.py \
  --archive /chemin/local/ForgePanel_Foundation_v0.7_source.zip \
  --destination "$HOME/forgepanel-intake/foundation-v07"

# Après création manuelle d'un parent privé, non accessible en écriture
# aux autres utilisateurs, copie explicite dans un dossier neuf :
mkdir -m 700 -p "$HOME/forgepanel-intake"
python3 scripts/stage_source_archive.py \
  --archive /chemin/local/ForgePanel_Foundation_v0.7_source.zip \
  --destination "$HOME/forgepanel-intake/foundation-v07" --stage
\`\`\`

L'option \`--stage\` déclenche la préparation ; **elle refuse root, les parents partagés ou modifiables par d'autres, les destinations déjà existantes, et les destinations internes au dépôt source**. L'option de test \`--evidence\` peut servir au diagnostic en lecture seule, mais **ne peut pas remplacer les preuves canoniques pour l'opération CLI \`--stage\`**.

## Contrôles concrets

- **Vérifier avant d'écrire** : identité SHA-256 du ZIP et 92 fichiers contre les preuves SRC-03 ; réutiliser le préflight R1 sans décompression sur disque.
- **Refuser les métadonnées risquées** : traversée, chemins absolus, doublons/collisions, noms Unicode non normalisés ou trompeurs, métadonnées \`.git\`, fichiers \`.env\` sensibles, symlinks/types spéciaux et modes setuid/setgid.
- **Copier sous contrôle** : ouverture de chaque répertoire via des descripteurs Linux \`O_NOFOLLOW\`, fichiers créés avec \`O_EXCL\` et mode **0600**, répertoires **0700**, aucune conservation de bits exécutables du ZIP.
- **Relire et comparer** : empreinte et taille de chaque fichier copiées avec celles du préflight ; nouvelle vérification du ZIP d'entrée ; en cas de divergence, arrêter et retirer le répertoire partiel.
- **Conserver la provenance** : générer \`.forgepanel-intake-receipt.json\` en mode 0600, avec empreinte ZIP, inventaire trié, empreintes de fichiers, \`STAGED_FOR_MANUAL_REVIEW\`, \`import_approved=false\` et \`executed=false\`. Cette pièce n'est **pas** un visa de sécurité.

**Ne jamais** lancer la commande depuis root ou copier le dossier de quarantaine tel quel dans le dépôt Core. L'emplacement doit appartenir à un utilisateur non privilégié. Toute revue de licences, secrets, dépendances, code et transformations de fichiers reste une étape séparée.

## Preuve et limites

La campagne \`python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v\` comprend **33 tests unitaires synthétiques** : 16 tests existants, 6 tests supplémentaires d'entrées ZIP dangereuses, et 11 scénarios de quarantaine. Les tests locaux sont passés ; le résultat exact CI sera enregistré dans la PR. L'intégrité des vrais octets SRC-03, le comportement Go/PHP, Symfony/PostgreSQL, les OS et les restaurations ne sont **pas vérifiés par ce lot**.

La destination privée et l'absence d'écrasement réduisent les effets de bord ; elles ne remplacent ni l'audit manuel, ni la preuve de confiance de l'éditeur. Suite : récupérer l'archive originale → préflight → quarantaine → revue des fichiers et licences → PR d'import R1 distincte → tests natifs Go/PHP → intégration R2. [Issue source #2](https://github.com/yyogas/forgepanel/issues/2).
