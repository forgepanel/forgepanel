<!-- forgepanel-doc id=FP-00-Q151-160 revision=1 status=specified -->
# Décisions Q151–Q160 — Certification reproductible, accès et avis de sécurité

[English](../../en/00-project-control/decisions-q151-q160.md) · [Q141–Q150](decisions-q141-q150.md) · [Qualification MVP](mvp-qualification.md) · [Contrats techniques](../02-architecture/qualification-and-security-contracts.md)

## Choix confirmés du propriétaire — 5 novembre 2026

**Q151 A, Q152 C, Q153 C, Q154 C, Q155 C, Q156 C, Q157 C, Q158 C, Q159 C, Q160 C**, sans remplacement de **Q1–Q150**. État : **SPECIFIED**, pas IMPLEMENTED/VERIFIED/RELEASED. Le Core AGPL complet reste utilisable sans Hub, MFA administrateur facultatif et marque unique par organisation.

| Réf. | Choix explicite | Exigence et limite |
|---|---|---|
| Q151 A | **QEMU/KVM local d'abord, pilotes VM cloud ensuite** | Implémenter/qualifier d'abord le premier pilote VM système QEMU/KVM et conserver le contrat multi-pilotes Q141 D. Vérifier l'accès KVM et les capacités du runner avant de promettre une CI VM ; cloud non obligatoire au premier jalon. |
| Q152 C | **Matrice interne, rapports signés, provenance, snapshots et historique** | Rattacher chaque test à image OS/arch, commit, configuration et outil, résultats PASS/FAIL/SKIP, instantané et scénario d'échec, empreinte/signature vérifiable, révision et historique. **Pas de publication officielle de matrice** imposée par Q152 C (option D non choisie). |
| Q153 C | **Blocage des régressions selon criticité/budgets, exception approuvée et auditée** | Budgets Q142 par classe d'application et environnement comparable ; refus selon niveau de régression, seuil et politique. Dérogations identifiées, limitées et journalisées ; **jamais de dérogation à un veto de sécurité/isolation/reprise Q132**. Pas de seuil numérique présumé. |
| Q154 C | **Vérifier uniquement les familles d'IP publiées (A/AAAA) et leur compatibilité HTTP-01** | Si A seul, contrôler IPv4 ; si AAAA seul, IPv6 ; si les deux, tester **les deux** sur les destinations/routes publiées. Ne pas imposer un AAAA inexistant ni ignorer une route IPv6 incorrecte. Prévisualiser enregistrements Q143, retester sans modification automatique. |
| Q155 C | **Redémarrage et mises à jour OS par politique serveur, approbation, backup, santé/récupération** | Préflight, approbateur autorisé, maintenance/reboot selon politique propre à l'hôte, snapshot récupérable, vérification état panneau et site, journal et procédure de secours. Orchestration multi-serveurs ultérieure Q144, pas requise au MVP. |
| Q156 C | **Exporter clé de récupération protégée, vérifier périodiquement son accessibilité ET restaurer isolément** | Une archive chiffrée Q135 n'est déclarée « récupérable » qu'après exercice de déchiffrement/restauration sur VM/environnement isolé avec vérification des données et droits ; coffre/copied key hors panne commune. **KMS externe/multi-gardiens restent facultatifs** (Q145 D), Q156 D non retenue. |
| Q157 C | **Gestion par le gestionnaire des clés SFTP, bornée au site, expiration, audit, validations sensibles** | Déposer/retirer des **clés publiques** sous politique du compte ; vérifier possession selon flux de sécurité, racine de site, quotas, durée/révocation et journal. Opérations sensibles soumises à validation ciblée. Aucun shell implicite, clé privée client collectée ni droit sur site tiers. |
| Q158 C | **Rapports manuels + santé locale + diagnostics minimisés à consentements séparés et seuils par cohorte** | Bêta Q137/Q147 contrôlée par signaux locaux, rapports testeurs et données sélectionnées volontairement ; consentements distincts pour version/diagnostic/autres usages Q6. Les seuils de pause sont par vague/cohorte, sans forcer la télémétrie ou communiquer fichiers/SQL/mail. |
| Q159 C | **Risque transfert premium : ancien serveur perdu, transferts répétés/inhabituels, identité/org incohérente ou compromission suspectée** | En cas de critère à risque, appliquer la **seconde approbation configurable Q138 D**, contrôle d'identité et preuve de possession Q148 C, suivi des décisions/rejets et secours manuel sécurisé. Ne pas inférer règles arbitraires par produit ou dérogation libre (Q159 D non choisie). Hub après ABI. |
| Q160 C | **Avis signés FR/EN lisibles sur site/Panel ET structurés lisibles machine**, notifications configurables | ID/version/signature, sévérité, produits/versions affectés, correctif, publication et divulgation coordonnée Q150, avec restriction des éléments sensibles. **Pas d'obligation de formats d'interopérabilité avancés** (option D non choisie) ni connexion Hub imposée au Core. |

## Précisions du périmètre de livraison

La première qualification R3 de Q119/Q120 démarre **avec QEMU/KVM local**. Les runners CI et cloud Q141 sont des extensions à qualifier selon leurs capacités ; les rapports communs et signés assurent la comparabilité sans attribuer un statut `PASS` à une VM non exécutée. Les budgets de performance **n'autorisent jamais de contourner les critères éliminatoires de sécurité**. Le premier site reste PHP avec **DNS externe**, ACME **HTTP-01** et HTTPS ; l'assistant Q154 contrôle uniquement les familles A/AAAA **réellement publiées**. Pour R4 : politique de reboot par serveur, backup chiffré avec **preuve de restauration isolée**, SFTP sans shell et gestion des clés publiques au niveau du site.

La **bêta privée** débute après preuves R4 et règles de distribution Q127, avec contrôles santé par cohorte, diagnostics minimisés et **consentements séparés**. Le **Hub** reste après l'ABI neutre R5 : Q159 complète les transferts cryptographiques/risqués Q128/Q138/Q148 ; Q160 complète avis signés et divulgation coordonnée Q140/Q150.

## Tests et refus attendus

- VM KVM indisponible, runner cloud non activé, snapshot défectueux, rapport falsifié/ancienne provenance, `SKIP` présenté en réussite : refuser la certification.
- Régression importante selon budget applicatif ; exception signée/auditée sur performance **seulement**, rejet systématique si fuite tenant ou panne de reprise.
- A sans AAAA : ne pas signaler IPv6 absent comme une panne. A+AAAA : échouer si **une famille publiée** conduit à un mauvais hôte/HTTP-01 ; retester HTTP/HTTPS sans modifier DNS.
- Mise à jour nécessitant reboot hors fenêtre/autorisation, sauvegarde invalide, health-check échoué : bloquer/reprendre explicitement.
- Archives déchiffrables uniquement avec clé perdue, coffre inaccessible ou restauration isolée incomplète : marquer **non récupérable**.
- SFTP clé publique non autorisée, accès expiré/révoqué, symlink hors site, dépassement quota et modification sensible non approuvée.
- Bêta sans consentement diagnostics : le Core reste utilisable, les signaux locaux/rapports manuels restent possibles ; pause de cohorte au seuil.
- Hub : serveur prétendument perdu, transferts rapprochés, organisation incohérente, soupçon de compromission ; deuxième validation lorsque politique de risque le requiert. Avis non signé/mal ciblé ou fuite d'exploit : rejet.

[Contrats et tests Q151–Q160](../02-architecture/qualification-and-security-contracts.md).

## Détails non choisis

Images VM/builds et runners KVM exacts, infrastructure de signature des rapports, seuils et criticité de budgets, politique de maintenance/reboot par défaut, méthode d'export des clés de secours, durée SFTP, champs/consentements diagnostics par cohorte, seuils antifraude, format structuré exact des avis/serveur web de publication et périodes de divulgation. **Ne pas inventer un fournisseur, seuil, protocole ou domaine.**
