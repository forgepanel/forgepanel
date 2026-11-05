<!-- forgepanel-doc id=FP-13-Q151-MATRIX revision=1 status=specified -->
# MVP : tests et portes de qualification Q151–Q160

[English](../../en/13-tests-quality/mvp-gates-q151-q160.md) · [Décisions](../00-project-control/decisions-q151-q160.md) · [Architecture](../02-architecture/qualification-and-security-contracts.md) · [MVP existant](../00-project-control/mvp-qualification.md)

**Tous les cas sont PLANNED, et non PASS.** La réussite d'un contrôle de documentation ne valide aucune VM, restauration, API Hub, connexion ACME ou mise à jour de serveur. Les résultats futurs devront préciser commit, image/OS, runner, WebStack, versions, snapshots, preuves/signatures, résultat PASS/FAIL/SKIP, environnement et responsable.

| Test ID | Jalon | Scénario réussi attendu | Cas de refus obligatoire |
|---|---|---|---|
| MVP-Q151-01 | R3 | VM système QEMU/KVM locale, snapshot, installer puis panne/reprise | KVM indisponible ou test conteneur seul → BLOCKED/SKIP, jamais OS qualifié |
| MVP-Q152-01 | R3 | Rapport de matrice **interne** signé, provenance image/commit/outils, snapshots/historique | Signature/empreinte altérée, rapport sans snapshot, PASS sur test SKIP → rejeter preuve |
| MVP-Q153-01 | R3 | Budget de performance par application, régression selon gravité et seuil | Exception de performance expirée/non approuvée ; faille inter-tenant, sécurité ou restauration Q132 → veto absolu |
| MVP-Q154-01 | R4 | A seul : IPv4 ; AAAA seul : IPv6 ; A+AAAA : les deux avec HTTP-01/HTTPS | Famille publiée inaccessible, port 80/challenge/TLS en panne → FAIL ; IPv6 non publié ne bloque pas |
| MVP-Q155-01 | R4 | Plan de paquets/reboot par serveur, approbation, backup récupérable et contrôle santé | Reboot non approuvé, backup non vérifié, panne après reboot, autre serveur affecté → stop/audit/récupération |
| MVP-Q156-01 | R4 | Clé de récupération exportée de façon protégée, accessibilité vérifiée, restauration isolée PASS du backup exact | Clé perdue/coffre indisponible, accès périodique raté, restore incomplet → pas de statut « récupérable » |
| MVP-Q157-01 | R4 | Gestionnaire autorisé ajoute/révoque **clé publique** SFTP par site, expiration, quota, approbation sensible | Clé privée demandée, shell, clé expirée, traversée site/symlink ou action non approuvée → refus |
| MVP-Q158-01 | Post-R4 | Bêta : rapports manuels + santé locale, diagnostic optionnel/minimisé et consentements distincts ; pause par cohorte | Refus/révocation de consentement, cohorte sous seuil, fuite de données ou santé critique → collecte refusée/pause |
| MVP-Q159-01 | Hub R6 | Transfert autorisé après contrôle org/installation, nonce neuf et seconde approbation selon risque | Hôte perdu sans vérification, transferts rapprochés, org incohérente ou compromission suspectée → gel ciblé |
| MVP-Q160-01 | Hub R6 | Un avis signé à contenu équivalent : **FR et EN humains** + **format structuré machine**, notification ciblée | Signature invalide, divergence de versions, destinataire erroné ou détail sensible exposé → refus/escalade |

## Règles de validation

**R3** : vraie VM KVM, provenance vérifiée et rapport **interne** signé ; aucun SKIP certifiant, aucune dérogation à Q132. Les exceptions Q153 ne concernent que les budgets de performance non critiques. **R4** : tester chaque famille A/AAAA réellement publiée et compatible HTTP-01 ; mise à jour/reboot par serveur autorisés avec backup **effectivement restaurable** ; statut RECOVERABLE seulement après contrôle périodique de clé et restauration isolée PASS ; accès SFTP par **clés publiques** et site. **Après R4** : cohorte bêta peut fonctionner sur santé locale/rapports manuels même sans télémétrie. **R5 puis R6** : extension neutre, ensuite tests Hub Q159–Q160 sur une intégration effective.

Les seuils exacts, durées, runners et formats restent à arbitrer. Cette matrice est une **spécification de tests**, pas un compte rendu exécuté.
