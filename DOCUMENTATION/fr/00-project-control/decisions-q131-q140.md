<!-- forgepanel-doc id=FP-00-Q131-140 revision=1 status=specified -->
# Arbitrages Q131–Q140 — Qualification VM, MVP, bêta et sécurité

[English](../../en/00-project-control/decisions-q131-q140.md) · [Décisions Q121–Q130](decisions-q121-q130.md) · [Qualification MVP](mvp-qualification.md) · [Roadmap technique](implementation-roadmap.md)

## Décisions confirmées par le propriétaire — 5 novembre 2026

Les choix **Q131 D, Q132 D, Q133 C, Q134 C, Q135 B, Q136 C, Q137 D, Q138 D, Q139 C, Q140 C** complètent **Q1–Q130** sans les remplacer. Ils sont au statut **SPECIFIED**, et ne constituent ni une qualification OS, ni un installateur/site opérationnel, ni une bêta réellement ouverte.

| Réf. | Décision | Règles d'administration et limites |
|---|---|---|
| Q131 D | **VM locales + CI automatisée + snapshots, pannes simulées et rapports par OS** | Chaque test indique OS/version/architecture, image, WebStack, build/commit, outils, étapes, journal expurgé, succès/échec/skip, évaluation sécurité et récupération. Un `SKIP` n'est pas un `PASS` ; un test en conteneur n'est pas une VM système. |
| Q132 D | **Qualification WebStack : compatibilité, sécurité, charge, maintenance, récupération et critères éliminatoires** | Tests applicatifs/PHP/`.htaccess`, listeners/TLS, isolation, disponibilité et retour après panne ; scénarios éliminatoires : fuite inter-tenant, contrôle d'accès contourné, collision de ports, impossibilité de récupération. Les mesures de charge ne remplacent pas la sécurité. **Aucune WebStack initiale présélectionnée** (Q122). |
| Q133 C | **Diagnostic externe DNS A/AAAA, port 80, chemin HTTP-01 et HTTPS** | Avertir des conflits A/AAAA/IPv6, propriétaire du site et vhost, challenge accessible publiquement en HTTP, certificat valide et HTTPS sur 443 ; donner des diagnostics actionnables sans exposer les tokens ACME. Pas d'obligation d'un fournisseur DNS local au MVP. |
| Q134 C | **Mises à jour OS avec créneau, plan d'impact, sauvegarde, health-check et récupération** | Liste de paquets/versions et services affectés, origine de confiance, permissions RBAC, préflight, snapshot d'état réellement récupérable, confirmation, suivi idempotent, alertes reboot et vérification des services/panneau/site. Aucune interface shell root arbitraire. |
| Q135 B | **Sauvegarde initiale chiffrée locale + destination distante facultative** | Couverture Q126 : configuration panneau + fichiers du site PHP, manifestes d'intégrité et **restauration réellement testée** ; sauvegarde de l'état PostgreSQL du panneau selon ce qui est nécessaire à la récupération. Une destination distante est optionnelle selon pilote disponible ; la sauvegarde locale chiffrée ne garantit pas la survie à une panne complète du disque. Les politiques 3-2-1/immutabilité Q65/Q75 restent à venir. |
| Q136 C | **Rôle gestionnaire de site : PHP/domaines/TLS/fichiers, SFTP et backup/restore sous politiques/quotas** | Permissions par organisation/site, opérations sensibles revalidées Q47, refus du root et des autres sites ; l'accès à une restauration ne donne pas le droit d'accéder aux données d'un autre compte, ni d'augmenter ses quotas. Admin système conserve les actions OS/paquets. |
| Q137 D | **Bêta privée : invitations/conditions, canal de bugs/mises à jour, vagues, pause/suspension et récupération** | Après VM internes et validation Q127, vagues de testeurs explicitement autorisés, version/artefact identifié, droit de retirer l'accès au canal et procédure de récupération. **Révoquer l'accès à la bêta n'efface pas automatiquement les droits logiciels déjà accordés aux destinataires ni leurs données.** |
| Q138 D | **Transfert premium : identité/org, preuve cryptographique, garde-fous, deuxième validation configurable pour les cas risqués** | Preuve de possession du nouveau serveur, plafonds/fréquence, anti-rejeu, journaux, révocation/ancienne affectation selon contrat ; serveur perdu : mode de récupération manuelle, approbation renforcée selon risque. Fonctionnalité du **Hub après ABI**, pas dans le MVP. |
| Q139 C | **Obligations partenaires : gravité, alertes automatiques, escalade et retrait** | Chaque version reste revue manuellement (Q114), critères contractuels Q129, délais convenus (non inventés), preuves de notification/remédiation, suspension/retrait en préservant le Core gratuit et les données clients. Hub différé. |
| Q140 C | **Signalement privé : niveaux de gravité, triage, correctifs, avis et communications coordonnées** | Responsable sécurité + suppléant Q130, suivi restreint, protection des données techniques, coordination des versions/correctifs et communication aux clients. GitHub privé + adresse dédiée Q118 doivent être **réellement configurés et testés** avant la bêta externe. |

## Définition de « première version réellement testable »

Les jalons **R1–R6 de Q120 D** restent inchangés. Pour **R3/R4 (MVP Q119 B)**, Q131–Q136 exigent maintenant :
- **R3** : matrice VM reproductible (local + CI lorsque l'infrastructure permet des VM système), snapshots/fault injection, comparaison des OS et WebStacks avec critères éliminatoires ; **aucun premier OS/WebStack choisi** avant preuves (Q121/Q122).
- **R4** : premier site PHP + domaine utilisant **DNS externe** + ACME **HTTP-01** + HTTPS, vérifications A/AAAA et ports 80/443 ; admin + gestionnaire de site (MFA facultatif), diagnostics VPS, gestion contrôlée de mises à jour OS avec récupération, sauvegardes chiffrées locales de configuration/fichiers et restauration **réelle**. Destination distante facultative.
- **Distribution** : tests internes isolés, puis seulement **bêta privée par vagues** après conditions légales/techniques, canaux sécurité vérifiés, responsable et suppléant réellement nommés.

Les objectifs multi-serveurs, DNS autoritatif, DNS-01/wildcards, WebStacks multiples, SFTP/backup avancés, HA et Hub restent prévus ; la décision Q136 précise **la portée de droits à viser** dans le MVP et n'est pas une preuve qu'un gestionnaire SFTP opérationnel est livré.

## Tests négatifs et critères de refus

Bloquer une WebStack présentant une faille `.htaccess`/tenant malgré de bons chiffres de charge ; échouer si DNS A et AAAA pointent vers des hôtes différents non approuvés, port 80 inaccessible ou challenge mal routé ; simuler panne réseau au milieu d'un upgrade OS et vérifier que le panneau et le site restent récupérables ; restaurer fichiers/config depuis backup chiffré avec secret disponible et signaler les limites si perte du disque ; refuser gestionnaire de site sur site tiers, augmentation de quota et mise à jour OS ; tester suspension de canal bêta sans destruction des données, transfert de licence concurrent/double affectation et traitement d'incidents partenaires.

## Sujets encore ouverts

Infrastructure concrète des VM/CI, métriques et seuils de charge éliminatoires, méthode de chiffrement/coffre des clés de sauvegarde, premier fournisseur de destination distante, politique de renouvellement des domaines, politique d'approbation OS, détails SFTP sur le tout premier site, contrats et quotas de bêta, preuves cryptographiques de transfert, délais partenaires et personnes/contact sécurité. **Aucune valeur numérique, fournisseur, personne ou adresse n'est inventé.**
