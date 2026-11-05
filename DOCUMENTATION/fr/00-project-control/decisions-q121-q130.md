<!-- forgepanel-doc id=FP-00-Q121-130 revision=1 status=specified -->
# Décisions Q121–Q130 — Première qualification, bêta privée et gouvernance

[English](../../en/00-project-control/decisions-q121-q130.md) · [Décisions Q111–Q120](decisions-q111-q120.md) · [MVP et tests](mvp-qualification.md)

## Décisions du propriétaire (5 novembre 2026)

**Q121 D, Q122 D, Q123 A, Q124 B, Q125 B, Q126 B, Q127 B, Q128 D, Q129 C, Q130 C** complètent Q1–Q120 ; elles ne remplacent pas les ambitions déjà approuvées. Statut **SPECIFIED**, pas IMPLEMENTED, VERIFIED ou PUBLISHED.

| ID | Choix validé | Portée et limites |
|---|---|---|
| Q121 D | Premier OS **sélectionné après comparaison de tests VM et prérequis** | Comparer les six OS ciblés selon installabilité, dépendances, confinement, mises à jour, diagnostics et reprise. **Aucun premier OS choisi**. Certifier chaque OS séparément. |
| Q122 D | Première WebStack **après tests de compatibilité et de sécurité** | Comparer profils disponibles, TLS, PHP-FPM, `.htaccess`, propriété des listeners, isolation et récupération. **Aucun profil de première version imposé**, la recommandation par site Q79 subsiste. |
| Q123 A | **DNS externe déjà configuré + validation ACME HTTP-01 + HTTPS automatique** pour la v1 | Le gestionnaire indique les enregistrements requis ; prouver résolution DNS, contrôle de domaine, disponibilité du challenge HTTP sur port 80 et HTTPS valide. **DNS autoritatif natif et pilote DNS-01 non requis au MVP**, conservés dans la roadmap. |
| Q124 B | **Administrateur local sécurisé + récupération + rôle gestionnaire de site** | Authentification permanente, sessions, CSRF, permissions admin et gestionnaire de site, interdiction d'accès aux sites d'autrui ; MFA administrateur **facultatif**. Pas de SSO/OIDC obligatoire en v1. |
| Q125 B | **État système, ressources, services, logs + gestion contrôlée des paquets/mises à jour OS** | Inventaire/diagnostic lecture seule ; actions de paquets planifiées, autorisées, vérifiées, journalisées avec avertissement de redémarrage et récupération. **Pas de terminal root arbitraire**. |
| Q126 B | **Sauvegarde du panneau/configuration + fichiers du premier site PHP, restauration réellement testée** | Conserver copies, manifestes, accès/secret, intégrité et restauration dans un environnement isolé. La base SQL cliente, réplication/immutabilité 3-2-1 et sauvegardes mail sont des objectifs ultérieurs ; PostgreSQL du panneau doit disposer d'une reprise cohérente si son état est nécessaire à l'installation. |
| Q127 B | **Tests internes isolés puis bêta privée de testeurs autorisés** | Bêta seulement après preuves MVP, droits d'accès, canal de sécurité actif, procédures de récupération et revue des conditions de distribution. **Distribution privée à des tiers n'exempte pas d'obligations de licence**. Pas de bêta publique implicite. |
| Q128 D | **Transfert de licence en libre-service contrôlé + récupération manuelle de serveur perdu** | Preuve de possession/organisation, autorisations, plafond, audit, anti-rejeu/double affectation ; processus de récupération encadré sans mot de passe root. Fonctionnalité Hub **après API d'extension**. |
| Q129 C | **Engagements partenaires de maintenance et sécurité, délais/responsabilités contractuels, alertes et retrait** | Revue humaine de chaque version (Q114), contact sécurité, traitement des vulnérabilités, sanctions/retrait ; **aucun délai ou niveau contractuel inventé**. Hub différé. |
| Q130 C | **Responsable sécurité identifié + suppléant + triage/notifications coordonnés** | Rôles autorisés, escalade, suivi, confidentialité, preuve de disponibilité des canaux GitHub privé/email (Q118). **Aucune personne, adresse ou SLA actuellement assigné**. |

## Réconciliation et frontières

Le **MVP Q119 B** reste : installateur vérifié, CLI, wizard, identité/PG, premier site PHP + domaine externe + HTTPS, avec les ajouts Q124–Q126. **Q120 D** reste strict : sources → Symfony/PG → installateur → site/VPS → ABI neutre → Hub. **Q121 et Q122 ne désignent aucun premier OS ou WebStack** ; l'équipe les sélectionnera uniquement après preuve de qualification. La Q123 n'annule ni DNS local/externe (Q63/Q73) ni DNS-01/wildcard (Q84/Q95), mais les décale après le premier parcours de site. Les sauvegardes 3-2-1/DR (Q65/Q75) restent à développer ; Q126 borne l'acceptation initiale.

Avant de transmettre une bêta privée à des testeurs externes, examiner les droits de distribution AGPL/commerciaux (Q111), CLA/contributions tierces (Q112), conditions et documents à fournir aux destinataires et canaux de sécurité vérifiés (Q118/Q130). Un dépôt privé ne supprime aucune obligation contractuelle ou de licence.

Hub traite Q128–Q129 après validation de l'ABI ; aucun abonnement, transfert ou partenaire ne conditionne la connexion, l'hébergement ou la récupération du Core gratuit.

## Règles de validation

Comparer explicitement VM/OS et WebStacks avant sélection ; test DNS A/AAAA, HTTP-01 et HTTPS, y compris échecs 80/443, DNS/IPv6 et mauvais certificat. Tester login local/reprise, séparation administrateur/gestionnaire de site, contrôles refusés, gestion sécurisée des paquets sans actions arbitraires, backup et restauration des fichiers et configuration sur VM. Tester canal de sécurité, autorisations et support de la bêta avec acteurs réels avant invitation. Pour Hub futur : transfert concurrent, machine perdue, preuve de possession, conformité de version et révision partenaire, incident et retrait.

[Plan détaillé du MVP](mvp-qualification.md) · [Roadmap R1–R6](implementation-roadmap.md). **Tous les résultats système/commerciaux restent à obtenir.**
