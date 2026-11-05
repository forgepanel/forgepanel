<!-- forgepanel-doc id=FP-00-Q151-160 revision=1 status=specified -->
# Décisions Q151–Q160 — qualification, sécurité, récupération et notifications

[English](../../en/00-project-control/decisions-q151-q160.md) · [Q141–Q150](decisions-q141-q150.md) · [Architecture](../02-architecture/qualification-gates-q151-q160.md) · [Matrice MVP](../13-tests-quality/mvp-gates-q151-q160.md)

**Confirmées par le propriétaire le 5 novembre 2026.** Q1–Q150 sont conservées, sans nouvelle décision implicite. Toutes les décisions ci-dessous sont SPECIFIED, non IMPLEMENTED ni VERIFIED. Les détails non fournis des options « B » et « A + B » ne sont pas inventés.

| ID | Choix | Décision | Interprétation et contrôle |
|---|---|---|---|
| Q151 | A | QEMU/KVM local en premier, puis pilotes cloud | Q141 D local+cloud reste le but ; le cloud est une phase ultérieure, sans certification implicite. |
| Q152 | C | Choix B + rapports signés, provenance, snapshots, historique des résultats | Signatures et empreintes vérifiées, run/image/commit/snapshot rattachés, PASS/FAIL/SKIP et historique auditable. |
| Q153 | C | Blocage selon criticité/seuils, exception approuvée et auditée | Dérogation bornée, justifiée, expirante et non critique seulement ; les veto Q132 de sécurité/isolation/récupération restent éliminatoires. |
| Q154 | C | Vérifier uniquement les familles IP publiées, compatibles avec le challenge | A public = IPv4 ; AAAA public = IPv6 ; les deux si publiées, port 80/ACME HTTP-01 et TLS ; aucune écriture DNS automatique Q143. |
| Q155 | C | Politique de mises à jour OS par serveur avec approbation, backup, santé, récupération | Plans de paquets autorisés ; refus sans backup préalablement récupérable, approbation et procédure locale de reprise. |
| Q156 | C | Choix B + restauration isolée avant déclaration de sauvegarde récupérable | Vérifier clés hors domaine de panne, configuration/panneau, fichiers PHP et état PostgreSQL cohérent ; job terminé ≠ restore PASS. |
| Q157 | C | Choix B + expiration, limites de site, audit et validation sensible | Gestionnaire de site/SFTP sans shell, permission contextualisée, révocation et expiration, audit expurgé et approbation des opérations sensibles. |
| Q158 | C | Choix B + diagnostics minimisés, consentements distincts et seuils par cohorte | Pas de collecte obligatoire ; consentements Q6 par finalité, suppression des petits groupes, pas de secrets/données client non nécessaires. |
| Q159 | C | Choix B + incohérence d'identité/organisation ou compromission suspectée | Revue/gel de l'opération de transfert premium ciblée, approbation selon risque Q138, vérification manuelle ; Core libre inchangé. |
| Q160 | C | Choix A + B, notifications configurables et données sensibles protégées | Alertes partenaires et avis signés Q149/Q150 : destinataires/canaux autorisés, redaction, protection d'historique, obligations légales maintenues. |

## Réconciliation avec les règles précédentes

- **Q141 D ↔ Q151 A** : cible locale + cloud conservée ; débuter avec VM système KVM locales et des preuves réelles, puis ajouter les pilotes cloud sans prétendre les avoir testés.
- **Q132 D ↔ Q153 C** : exceptions approuvées uniquement sur risques/seuils non critiques ; isolation inter-tenants, sécurité bloquante ou restauration impossible ne peuvent devenir PASS.
- **Q123/Q143 ↔ Q154** : seul le DNS externe effectivement publié est testé ; A sans AAAA n'impose pas IPv6, mais AAAA cassé bloque le challenge.
- **Q135/Q145 ↔ Q156** : backup chiffré et coffre ne suffisent pas : restauration isolée et disponibilité des clés après panne commune.
- **Q136/Q146 ↔ Q157** : SFTP sans shell, portées de site et autorisations sensibles locales ; aucun shell privilégié arbitraire.
- **Q6/Q147 ↔ Q158** : télémétrie par consentements distincts, minimisation et protection de petites cohortes.
- **Q128/Q138/Q148 ↔ Q159** : transfert premium révisable sur identité/org/compromission, seconde approbation selon risque, autonomie du Core.
- **Q149/Q150 ↔ Q160** : notifications paramétrables et avis authentifiés avec données sensibles protégées ; aucun SLA ni canal inventé.

## Ordre technique et détails ouverts

**R3** : Q151–153 et qualification de l'OS/WebStack après preuves. **R4** : Q154–157 et MVP PHP/HTTPS/backup récupérable. **Après R4** : diagnostics et bêta sous Q147/Q158. **Après ABI neutre R5** : Hub R6 traite Q159/Q160. Le Core reste utilisable hors Hub.

Restent **OPEN** : fournisseur/runners cloud futurs, clé/format/signature/rétention des preuves, seuils et durée des exceptions, vérifications DNS multi-réseaux, fenêtres update, fréquence des restaurations, durée des accès, seuil minimal des cohortes, score de risque et canaux de notification. Aucune valeur chiffrée inventée.
