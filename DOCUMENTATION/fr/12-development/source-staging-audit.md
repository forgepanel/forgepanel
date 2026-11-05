<!-- forgepanel-doc id=FP-12-SOURCE-AUDIT revision=2 status=documented -->
# Vérification indépendante de la quarantaine R1

[English](../../en/12-development/source-staging-audit.md) · [Préflight](source-archive-intake.md) · [Préparation privée](source-staging.md) · [Audit et risques](../19-audits-risks/README.md)

## Objectif et statut

`scripts/audit_staged_archive.py` est un **outil en lecture seule** pour contrôler la quarantaine avant une revue manuelle. Il compare **trois objets** : (1) le ZIP original épinglé dans `DOCUMENTATION/evidence/sources.json`, (2) le reçu de staging `.forgepanel-intake-receipt.json`, et (3) les fichiers présents sur disque. Le fichier original `ForgePanel_Foundation_v0.7_source.zip` (SRC-03, 92 fichiers) reste **indisponible** dans ce contexte : aucun contrôle sur ses vrais octets, import PHP/Go ou test de runtime ne doit être revendiqué.

## Commandes

```bash
# Le ZIP d'origine doit encore être disponible.
python3 scripts/audit_staged_archive.py \
  --archive /chemin/local/ForgePanel_Foundation_v0.7_source.zip \
  --directory "$HOME/forgepanel-intake/foundation-v07"

# Tests du vérificateur, du staging et de cet audit, sur données fictives :
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
```

Les contrôles CLI utilisent le **registre canonique** SRC-03. Le programme n'extrait, n'exécute et ne modifie rien. `CONSISTENT_FOR_MANUAL_REVIEW` signifie : identités et empreintes de fichiers **cohérentes au moment de la lecture**, **pas** « code sûr », « import approuvé » ou « environnement de production certifié ». Toute anomalie produit `BLOCKED` et un code de retour 2.

## Invariants et refus

| Domaine | Contrôle |
|---|---|
| Archive d'origine | Le SHA-256 complet et le nombre de fichiers doivent correspondre à SRC-03 ; la signature d'éditeur, la licence et la confiance restent une revue indépendante |
| Reçu de provenance | Version/champs/types stricts, `import_approved=false`, `executed=false`, état `STAGED_FOR_MANUAL_REVIEW` ; empreintes du reçu égales à celles calculées depuis le **vrai** ZIP |
| Répertoire privé | Chemin absolu canonique et dossier non partagé appartenant à l'utilisateur ; refus des chemins d'accès symboliques et dossiers trop permissifs |
| Inventaire | Tous les fichiers réguliers attendus doivent exister ; refuser chaque fichier/dossier inattendu, manquant, remplacé ou à chemin dangereux |
| Intégrité fichiers | Vérifier SHA-256/taille et stabilité des métadonnées avant/après lecture ; refuser liens symboliques, liens physiques supplémentaires, FIFO, fichiers exécutables, permissions partagées, changement de propriétaire |
| Panne | Contrôles bornés de taille du reçu et des fichiers ; aucun verdict positif en cas de changement concurrent, disparition d'un membre ou archive modifiée |

## Amélioration du staging en complément

Le programme de quarantaine refuse dorénavant les **destinations relatives**, dossiers intermédiaires partagés et `--source-id` différent de SRC-03 en mode CLI `--stage`. Sa procédure d'échec ne supprime que le dossier de quarantaine associé à l'**identité inode/dev créée**, à travers le descripteur du parent privé. Si son nom a été remplacé entre-temps, le nettoyage est **abandonné et signalé** plutôt que de risquer de supprimer un dossier étranger. Le succès vérifie également la stabilité de l'identité du répertoire avant de rendre un reçu.

## Frontières et risques résiduels

Les tests de la branche s'appuient sur des archives **synthétiques** : aucun test d'intégration ne démontre le comportement de SRC-03, Symfony/PostgreSQL ou d'une installation Linux. Ce vérificateur n'est pas un antivirus, ne garantit pas l'absence de secrets cachés, ne vérifie pas les droits de licence et **n'empêche pas un acteur malveillant disposant du même UID de modifier les fichiers après la vérification**. Une future PR d'import devra relire et vérifier ces octets au moment de son propre import et conserver une piste de provenance versionnée ; elle ne pourra pas se contenter de ce seul rapport.

**Séquence obligatoire :** ZIP original → préflight signé au niveau du rapport/provenance disponible → copie privée → audit indépendant des octets → revue humaine sécurité/licence → PR d'import Core avec tests Go/PHP réels → intégration R2. Aucun `shell.exec`, aucune élévation Linux, aucune dépendance Hub.

**Validation synthétique observée :** campagne R1 complète de **60 tests**, exécutée avec succès sur la branche de PR #39. Ce nombre reflète les scénarios de code fictifs, pas des essais d'installation sur le véritable ZIP. Le vérificateur refuse également toute quarantaine située dans le dépôt source.
