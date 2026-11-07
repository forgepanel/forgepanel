<!-- forgepanel-doc id=FP-12-OPTIONAL-ADMIN-MFA-071 revision=1 status=documented -->
# Foundation v0.7.1 — correctif MFA initiale facultative (PR empilée)

[English](../../en/12-development/foundation-v071-optional-mfa.md) · [Import des sources](foundation-v07-source-import.md) · [Inventaire du patch](../../evidence/foundation-v071-optional-mfa-patch.json)

## Objet et périmètre exact

Le propriétaire a explicitement choisi la **MFA administrateur facultative**. Le prototype Foundation v0.7 imposait encore l'enrôlement TOTP initial avant la configuration. Le **patch candidat de 11 fichiers**, tiré octet pour octet de l'archive v0.7.1 MFA facultative retrouvée (SHA-256 `83fe6e77713f68d69595e74864aa1c33f75d88b6ba4199e03d5ef30a7060402c`), introduit un choix explicite de passer l'étape, protégé par le grant de setup courant, CSRF et limite de débit. Il supprime le secret d'enrôlement chiffré en attente, refuse un second saut, journalise l'événement sans secret et autorise ensuite la configuration. Les MFA déjà confirmées restent actives. **Une seule migration additive** après `001_setup.sql` : `ALTER TABLE fp_admins ALTER COLUMN mfa_secret DROP NOT NULL;`.

Le code ne démontre pas le fonctionnement HTTP Symfony, la concurrence PostgreSQL réelle ni une installation ForgePanel. Les 30 tests métier PHP (199 assertions) et tests Go natifs ont été exécutés sans privilège root ni base réelle. La revue sécurité devra examiner la transaction, les sessions/grants et le passage upgrade/downgrade SQL. Aucune version distribuée, signature ni certification runtime n'est revendiquée.

## Vérifications reproductibles

```sh
python3 scripts/check_foundation_import.py
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
bash scripts/check.sh
```

Le manifeste d'import v0.7 reste immuable ; le second registre de 11 fichiers fixe les empreintes avant/après. Le contrôleur refuse la modification des octets, une migration absente, les fausses validations de release et tout `.env` d'origine. `install apply` reste bloqué. Le patch est une PR empilée sur [l'import R1](foundation-v07-source-import.md) pour revue ciblée, **pas une autorisation de fusion**.

**Avant R2 :** vérifier réellement en HTTP Symfony HTTPS/origine/CSRF/navigateur le choix explicite « sans MFA » et l'enrôlement, les procédures de récupération du compte, la migration PostgreSQL ainsi que transactions/concurrence. Hub privé facultatif, décisions Q1–Q220 conservées.