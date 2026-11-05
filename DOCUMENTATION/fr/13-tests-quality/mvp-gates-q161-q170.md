<!-- forgepanel-doc id=FP-13-Q161-MATRIX revision=1 status=specified -->
# Matrice de tests MVP Q161–Q170

[English](../../en/13-tests-quality/mvp-gates-q161-q170.md) · [Décisions](../00-project-control/decisions-q161-q170.md) · [Tests antérieurs](mvp-gates-q151-q160.md)

**Tous les scénarios réels sont PLANNED, pas PASS.** Chaque preuve devra citer commit, OS, image, environnement, type de test, résultats et traces expurgées.

| Test ID | Phase | Réussite attendue | Refus obligatoire |
|---|---|---|---|
| MVP-Q161-01 | R3 | Runner KVM isolé et temporaire avec image figée, quotas, nettoyage et preuves préservées | VM conteneur seule, secret restant, image non approuvée, échec nettoyage : pas de qualification |
| MVP-Q162-01 | R3 | Rapport signé validé, historique accessible dans stockage privé immuable | Signature fausse, tentative modification historique ou accès RBAC non autorisé : refus |
| MVP-Q163-01 | R3 | Dérogation de performance non critique autorisée par rôle distinct et expirante | Auto-approbation, exception hors portée ou veto Q132 sécurité/restauration : blocage |
| MVP-Q164-01 | R4 | A uniquement, AAAA uniquement ou les deux vérifiés localement et depuis sonde externe pour HTTP-01 | IPv6 non publié : N/A ; AAAA cassé, sonde inaccessible ou SSRF : refus de conclure PASS |
| MVP-Q165-01 | R4 | Réparation non destructive avec checkpoint, limites de tentatives et health-check | Boucle illimitée, shell libre ou action risquée sans approbation : refus |
| MVP-Q166-01 | R4 | Chaque backup restauré isolément en totalité avant RECOVERABLE, exercices hôte/clé planifiés | Restauration incomplète ou omise, clé absente : pas de statut récupérable |
| MVP-Q167-01 | R4 | Clé SFTP publique prouvée, algorithme approuvé, portée site, expiration, rotation et audit | Clé privée, algorithme interdit, clé révoquée ou sortie de site : refus |
| MVP-Q168-01 | Bêta post-R4 | Consentement par finalité et cohorte suffisante, rapport agrégé expurgé | Consentement retiré, cohorte réidentifiable ou donnée secrète : aucun envoi |
| MVP-Q169-01 | Hub R6 | Transfert bas risque autorisé sous règle versionnée, revue des cas à risque | Nonce rejoué, org divergente, serveur perdu ou compromission : gel du transfert seulement |
| MVP-Q170-01 | Hub R6 | Avis signé JSON validé et même version FR/EN, notifications filtrées | Schéma invalide, signatures manquantes, désaccord FR/EN ou fuite donnée : refus |

**Critères de sortie** : R3 preuves KVM signées et non falsifiables, dérogations performance Q132 sûres ; R4 DNS local/externe, réparation OS bornée, restauration isolée **chaque backup** et gestion publique SFTP. Après R4, bêta par consentements ; Hub R6 après R5 pour transferts et avis JSON FR/EN. Un SKIP, un rapport signé seul ou une CI documentaire ne constituent jamais une qualification.
