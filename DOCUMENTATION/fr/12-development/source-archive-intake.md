<!-- forgepanel-doc id=FP-12-SOURCE-INTAKE revision=2 status=documented -->
# Préflight sécurisé d'une archive source R1

[English](../../en/12-development/source-archive-intake.md) · [Développement](README.md) · [Provenance](../19-audits-risks/baseline.md) · [Roadmap](../00-project-control/implementation-roadmap.md)

## Objet et statut

**Vérificateur de ZIP en lecture seule : IMPLEMENTED. Tests sur archives fictives : 16 PASS localement. Import du Core : BLOCKED.** L'archive originale SRC-03, \`ForgePanel_Foundation_v0.7_source.zip\`, n'est pas disponible dans les fichiers actuellement accessibles et n'a pas été importée.

Le registre [\`sources.json\`](../../evidence/sources.json) fixe SRC-03 à **92 fichiers** et l'empreinte SHA-256 \`19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a\`. **Une empreinte vérifiée prouve la correspondance au registre, pas l'authenticité d'un éditeur, la licence ni l'innocuité du contenu.**

## Utilisation après réception de l'archive originale

\`\`\`bash
python3 scripts/verify_source_archive.py --archive /chemin/local/ForgePanel_Foundation_v0.7_source.zip
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
\`\`\`

Le programme ne fait **aucune extraction, exécution, installation, modification Linux ni requête réseau**. Le rapport JSON local fournit l'empreinte du ZIP, le nombre de fichiers, les empreintes individuelles, les avertissements, les blocages et le statut \`PASS\` ou \`BLOCKED\`. Code de retour **0** = précontrôles réussis ; **2** = précontrôles bloqués. Un \`PASS\` ne donne jamais autorisation de lancer \`install apply\` ni de publier une release.

## Garanties mises en œuvre

- **Provenance** : comparer l'empreinte exacte à SRC-03 **avant de lire les membres** ; refuser l'archive divergente ou absente.
- **Chemins** : refuser ZIP Slip (\`..\`), chemins absolus ou Windows, composants vides, collisions de casse, doublons et conflit fichier/répertoire.
- **Types** : refuser liens symboliques, fichiers Unix spéciaux, entrées chiffrées et méthodes de compression non acceptées.
- **Bornes** : contrôler taille/compteur/ratio de compression, vérifier les données en flux par CRC et calculer les SHA-256 par membre.
- **Secrets** : bloquer quelques signatures reconnaissables de clé privée/token et les fichiers \`.env\` sans imprimer la valeur ; signaler les extensions de clés/certificats pour revue.

Les **limites défensives internes** du préflight sont 64 Mio pour le ZIP, 2 048 membres, 32 Mio par membre, 160 Mio décompressés au total et ratio 500. Il ne s'agit **pas de quotas commerciaux ForgePanel** ; une adaptation exige revue et test.

## Ce que ces tests ne prouvent pas

Les 16 tests utilisent des ZIP **synthétiques uniquement**. La recherche de secrets n'est ni exhaustive ni une revue juridique, la SHA ne remplace pas la vérification de la chaîne de confiance et une archive valide ne prouve pas la sécurité des sources PHP/Go, de Symfony/PostgreSQL ou du système d'exploitation. **Le vrai ZIP SRC-03 n'a pas été rescanné dans cette étape faute d'octets.**

Suite R1 sous [issue #2](https://github.com/yyogas/forgepanel/issues/2) : obtenir l'archive exacte → exécuter préflight → revue humaine des fichiers, licences, secrets, historique → importer uniquement les sources approuvées dans \`features/* → develop\` → tests Go/race/vet/PHP sur commit importé → R2 Symfony/PostgreSQL. [Relais](../18-contributing/handover.md).

## Étape complémentaire — préparation en quarantaine

Le [module de staging privé](source-staging.md) permet après contrôle préalable de préparer **les fichiers réguliers** dans un répertoire neuf hors dépôt, non-root, avec manifestes et comparaison de hash ; mode prévisualisation par défaut et option explicite `--stage`. **Ce n'est pas l'import applicatif R1**, toujours en attente de SRC-03.
