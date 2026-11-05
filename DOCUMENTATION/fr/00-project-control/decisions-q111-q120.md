<!-- forgepanel-doc id=FP-00-Q111-120 revision=1 status=specified -->
# Arbitrages Q111–Q120 — Gouvernance et première version

[English](../../en/00-project-control/decisions-q111-q120.md) · [ADR](decisions.md) · [Roadmap](implementation-roadmap.md)

## Choix du propriétaire — 5 novembre 2026

Ces décisions complètent **Q1–Q110**, sans les remplacer. Elles sont **SPECIFIED** et non implémentées.

| Réf. | Décision confirmée | Limites et exigences |
|---|---|---|
| Q111 C | AGPL-3.0 + commerciale ; variante après revue juridique | Choix only/or-later et texte commercial en attente. Aucun nouveau fichier LICENSE sans validation. |
| Q112 C | CLA électronique et vérification des droits individuels/entreprises avant fusion | Contrôler identité, autorité du signataire, consentement et preuve d'acceptation ; texte et plateforme à sélectionner. |
| Q113 D | Pools de licences par organisation, transferts et remplacement de serveur | Affectations bornées et auditables, prévention des doubles allocations et récupération en cas de serveur perdu ; pas de privilège Linux. |
| Q114 C | Revue manuelle de chaque version partenaire, obligations de maintenance et sécurité, retrait | Approbation par version et artefact, compatibilité, signature, canal de vulnérabilité et suspension contrôlée. |
| Q115 D | Pilotes de paiement testés en sandbox, puis prestataires par marché | Vérifier callbacks authentifiés, duplications, remboursements et concurrences ; aucun fournisseur pays/devise imposé. |
| Q116 C | Rétention par catégorie et juridiction configurable dans les limites légales | Base de traitement, contrôle des min/max, gel légal, purge et audit ; aucune durée universelle choisie. |
| Q117 C | Révocation premium motivée (sécurité, fraude, remboursement, expiration) | Règles et notifications selon motif, sans couper le Core gratuit ni effacer des données. Révocation connue ≠ grâce automatique de 60 jours. |
| Q118 C | Signalement privé GitHub et adresse sécurité dédiée avec triage, suivi et notifications | Activer et vérifier les deux canaux avant publication. Aucune adresse ou SLA n'est encore disponible. |
| Q119 B | Premier produit testable : installateur, CLI, wizard, identité/PostgreSQL et site PHP avec domaine/HTTPS | Prouver un vrai parcours install→admin→site PHP→HTTPS→gestion/récupération, avec preuves de tests. |
| Q120 D | Sources → Symfony/PostgreSQL → installateur → premier site/VPS → API d'extension → Hub | Ordre des dépendances impératif, documenté dans [la roadmap](implementation-roadmap.md). |

## Invariants

Core gratuit et autonome, double licence AGPL/commerciale sans variante exécutoire choisie, MFA administrateur facultatif, une marque par organisation, WebStack recommandée et changeable par site, Q47 pour les modifications sensibles. Les services premium restent facultatifs ; les droits commerciaux n'accordent pas de droits systèmes. Les 60 jours hors ligne de licence premium ne sont pas la grâce des quotas d'hébergement.

## Première livraison et preuves

Q119 **n'exige pas** toutes les fonctions prévues dans Q1–Q110 dès la v1 : pas de promesse de DNS autoritatif natif, mail, multi-serveurs, HA, marketplace, WebStacks multiples ni six OS certifiés d'emblée. Le premier site PHP avec domaine et HTTPS doit être réellement joignable sur un OS et un profil **testés**, après authentification, gestion de sessions, permissions et procédure de récupération. Le Hub ne précède pas la mise à disposition de l'API générique d'extension.

Le dossier source v0.7.1 corrigé du MFA existe en **archive distincte**, pas en code importé sur `develop`. Ne pas le représenter comme source Git déjà intégrée.

## Restent à arbitrer

Variante AGPL only/or-later, conditions commerciales, texte/outil de signature CLA, règles de pool et de transfert, critères partenaires, marchés/prestataires, catégories et durées réglementaires, matrice des révocations, adresse et contacts de sécurité vérifiés, OS/stack du pilote et critères d'essais de la v1. Ces détails ne sont pas choisis implicitement.
