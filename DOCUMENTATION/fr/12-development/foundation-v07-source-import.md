<!-- forgepanel-doc id=FP-12-FOUNDATION-SOURCE-IMPORT revision=1 status=documented -->
# Foundation v0.7 — import de sources candidat et contrôles reproductibles

[English](../../en/12-development/foundation-v07-source-import.md) · [Développement](README.md) · [Préflight R1](source-archive-intake.md) · [Manifeste](../../evidence/foundation-v07-import-candidate.json)

## Périmètre de cette PR source en brouillon

Cette PR **introduit le code source applicatif** de l'archive historique Foundation v0.7 **SRC-03** contrôlée par SHA-256, mais **n'installe, ne déploie, ne publie, ne signe, n'active ni ne certifie** un panneau d'hébergement. Le lot de 66 fichiers contient 64 sources originales identiques octet par octet et deux chemins adaptés et identifiés : `.gitignore` durci et `apps/panel/.env.example` sans secret. Le fichier original `apps/panel/.env`, la documentation historique, les anciens résultats de tests et l'ancien changelog sont **exclus**. Le ZIP d'origine reste conservé en privé, jamais ajouté au Git public.

Le registre `DOCUMENTATION/evidence/foundation-v07-import-candidate.json` fixe tous les chemins, tailles et SHA-256 ainsi que le SHA-256 SRC-03 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`. L'outil `scripts/check_foundation_import.py` contrôle les octets, les absences, les liens symboliques et les fichiers d'environnement. Il s'agit d'un contrôle d'intégrité, **pas d'une preuve d'authenticité, de licence ni d'un audit de sécurité**.

## Contrôles reproductibles sur commit importé

```sh
python3 scripts/check_foundation_import.py
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go vet ./...
php apps/panel/tests/run.php
bash scripts/check.sh
```

La CLI Go `install plan` reste expressément **non exécutable** ; `install apply` est refusé. Les tests métier PHP sont isolés ; les tests HTTP Symfony, les transactions PostgreSQL, les sessions, les permissions, l'installation OS/VM, les upgrades et restaurations sont **NOT RUN**. La v0.7 impose encore TOTP au setup ; le choix du propriétaire exige **MFA administrateur facultative**, via le patch v0.7.1 **séparé**, à auditer notamment côté SQL/HTTP avant de déclarer un parcours complet.

## Conditions de publication, revue et reprise

- Examiner la provenance exacte, les droits tiers et les termes AGPL/commerciaux. L'ancien `LICENSE-NOT-SELECTED.md` n'accorde aucune licence ; cette PR ne sélectionne pas de texte légal définitif.
- Confirmer l'absence de secrets de production. `.env.example` n'est qu'un modèle. Ne jamais commiter `.env`, `.env.local`, binaires, ni clés de signature privées.
- Examiner indépendamment le pont privilégié, les chemins Linux, bornes d'entrée, migrations SQL, reprise et isolation des sessions/origines ; l'absence de shell arbitraire ne vaut pas validation de runtime.
- Réexécuter la CI sur SHA exact, puis les vrais tests Symfony/PostgreSQL/OS/VM selon R2/R3/R4.
- Aucune fusion/promotion avant réconciliation de la documentation et validation des blocages légaux/sécurité par les responsables autorisés. Le Core reste gratuit et autonome sans Hub privé. Préserver Q1–Q220 et le workflow `features/* → develop → stable → main → production`.