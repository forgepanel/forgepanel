<!-- forgepanel-doc id=FP-13-Q151-MATRIX revision=1 status=specified -->
# Tests MVP Q151–Q160 — matrice de qualification

[English](../../en/13-tests-quality/mvp-gates-q151-q160.md) · [Décisions](../00-project-control/decisions-q151-q160.md) · [MVP](../00-project-control/mvp-qualification.md)

**État de tous les tests : PLANNED, pas PASS.** Relever commit, OS/version, runner, image et snapshots, outils, résultat PASS/FAIL/SKIP et preuve réelle ; CI documentaire ≠ tests VM ou restauration.

| Test ID | Phase | Succès à démontrer | Refus impératif |
|---|---|---|---|
| MVP-Q151-01 | R3 | VM QEMU/KVM réelle + snapshot + install/reprise | Conteneur seul ou SKIP ne qualifie pas l'OS |
| MVP-Q152-01 | R3 | Rapport signé, empreinte, provenance et historique vérifiés | Signature invalide/artefact absent/historique incohérent → refus |
| MVP-Q153-01 | R3 | Seuil non critique et dérogation limitée approuvée | Dérogation expirée ou veto Q132 critique → FAIL, jamais PASS |
| MVP-Q154-01 | R4 | A seulement, AAAA seulement et A+AAAA : HTTP-01/TLS par famille publiée | AAAA publié inaccessible ou challenge port 80 défaillant → refus ; IPv6 absent non pénalisé |
| MVP-Q155-01 | R4 | Mise à jour par serveur approuvée, backup récupérable et santé contrôlée | Backup non vérifié/échec update/impact sur autre serveur → arrêt et audit |
| MVP-Q156-01 | R4 | Restore sur VM isolée PASS avec clés et état PHP/panneau/PG | Restore échoué ou omis → statut recoverable interdit |
| MVP-Q157-01 | R4 | Accès temporaire par site, SFTP sans shell et approbation sensible | Accès expiré, symlink inter-tenant ou action sans approbation → refus |
| MVP-Q158-01 | Post-R4/Hub R6 | Consentement par finalité et cohortes anonymisées au seuil | Cohorte trop petite, révocation ou diagnostic sensible → suppression |
| MVP-Q159-01 | Hub R6 | Transfert correct et approbations selon risque | Identité/org discordante, suspicion compromission ou nonce rejoué → gel ciblé |
| MVP-Q160-01 | Hub R6 | Avis signé diffusé par canal autorisé | Secret dans avis, destinataire incorrect, signature invalide → refus/escalade |

**R3** : KVM qualifié, rapport signé, politique et veto Q132. **R4** : HTTP-01 sur IP publiées, backup réellement restauré isolément, OS updates autorisées et SFTP limité. **R5** : extension neutre testée sans Hub. **Hub R6** : consentements, risque commercial, avis protégés. Les seuils, délais et fournisseurs restent OPEN. Les tests documentaires vérifient seulement la cohérence de cette matrice, pas sa réalisation. [Contrats](../02-architecture/qualification-gates-q151-q160.md).
