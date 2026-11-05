<!-- forgepanel-doc id=FP-00-POLICY revision=1 status=documented -->
# Décisions produit du 5 novembre 2026 — gratuit, commercial et configurable

[English](../../en/00-project-control/product-policy.md) · [Registre ADR](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## Décisions du propriétaire (confirmées, mais pas implémentées)

| Référence | Décision | Portée et invariants |
|---|---|---|
| Q1 | Double licence | Modèle confirmé ; **les textes exacts, détenteurs de droits, contributions et exceptions restent ouverts**. Aucun fichier LICENSE n'est sélectionné. |
| Q2 | Core complet et gratuit + premiums + support | Fonctionnalités d'hébergement fondamentales et récupération disponibles sans licence payante ni Hub ; les offres premium portent sur des services/composants facultatifs clairement définis. |
| Q3 | Tous publics par phases | Hébergement mutualisé et VPS d'abord ; développeurs et revendeurs ensuite, avec contrats extensibles sans promesse de fonctionnalités déjà livrées. |
| Q4 | PHP + Node.js + Python + conteneurs | Runtimes applicatifs configurables, séparés du PHP du panneau ; l'automatisation du Core reste Go/Symfony, Python non obligatoire. Moteur conteneur exact à choisir. |
| Q5 | White-label étendu par organisation | Nom, logo, favicon, couleurs, thèmes, domaines/HTTPS, emails/templates et portail par organisation ou revendeur ; privilèges soumis au RBAC, isolation des cookies/sessions et validation des domaines. |
| Q6 | Enregistrement et contact Hub avec consentements séparés | Installation standard autonome ; gestion explicite des canaux enregistrement, droits premium, vérification de versions, statistiques limitées, diagnostics/support et communications. Pas de collecte implicite des données d'hébergement. |
| Q7 | Tolérance hors ligne **60 jours** | Pour droits premium auparavant vérifiés, selon contrat produit et expiration effective ; pas d'arrêt des services essentiels ni de suppression destructrice. La règle de révocation, source de temps et cas d'expiration restent à préciser. |
| Q8 | Catalogue officiel + partenaires validés | Catalogue de distribution gouverné par l'éditeur, partenaires approuvés avec vérification identité, signatures, compatibilité et revue ; pas de publication publique libre pour le moment. |
| Q47 | Changement sensible avec plan/validation/sauvegarde/récupération | Exposer impact, test de configuration, sauvegarde avant modification, vérification post-application et compensation/récupération quand possible. Un rollback universel SQL/OS n'est pas promis. |

Ces décisions s'ajoutent à ADR-013 : **MFA administrateur facultatif**, proposé sans bloquer le premier setup. Un choix commercial ou de présentation ne peut jamais contourner l'autorisation locale ni les droits Linux.

## Séparation Core gratuit / services commerciaux

Le Core couvre l'installation, le compte administrateur, la gestion des comptes et sites, l'isolation, les domaines, le SSL, l'accès aux fichiers, l'administration des services natifs retenus, les quotas, sauvegardes et récupération. La liste exacte de fonctionnalités minimales de la release reste à établir par critères d'acceptation.

Les offres premium peuvent porter sur des extensions non essentielles, services managés, support prioritaire, offres partenaires, hébergement de catalogue ou outils spécialisés. Une fonctionnalité de sécurité déjà nécessaire au Core ne devient pas payante par renommage. La facturation et les droits commerciaux appartiennent au Hub, pas au chemin de démarrage ou de récupération du Core.

## Politique des 60 jours — spécification de principe

Le Hub peut émettre des preuves de droits vérifiables localement. Le client conserve la dernière preuve authentique connue ; une panne réseau place le droit en état `offline-grace` pour **au plus 60 jours depuis la dernière vérification positive**, sans dépasser une échéance contractuelle explicitement opposable. Le comportement à expiration commerciale, révocation, changement d'horloge ou absence de première validation doit être précisé avant implémentation. Aucune commande distante ne doit arrêter les sites clients. Ce délai concerne les droits optionnels, jamais la capacité d'utiliser le Core complet gratuit.

## Personnalisation et permissions

Les choix UI peuvent être surchargés par organisation dans les limites de la politique du serveur. Les réglages sensibles nécessitent autorisations effectives et traçabilité : une permission de white-label ne donne pas accès aux clés de certificats privées ou aux comptes clients étrangers. Les utilisateurs peuvent consulter les valeurs héritées et pourquoi certaines options sont verrouillées.

## Questions encore ouvertes — ne pas présumer

- **Q48** : licence libre exacte de la double licence (AGPL-3.0-only / GPL-3.0-only / autre) et forme commerciale.
- **Q49** : clauses contributions/CLA et stratégie de dépendances tiers ; vérifier la chaîne de titres avant double licence.
- **Q50** : limites exactes du Core gratuit vs composants premium (catalogue de fonctionnalités contractuel).
- **Q51** : Docker ou Podman (ou plusieurs pilotes) et isolation des conteneurs/runtimes client.
- **Q52** : politique des 60 jours en cas de licence expirée, explicitement révoquée ou jamais validée ; avertissements et non-destruction.
- **Q53** : modèle de validation des partenaires et responsabilité des mises à jour.
- **Q54** : ordre précis des prochains modules dans les phases.
- **Q55** : domaines/identités revendeurs, contraintes de white-label et certificats, anti-usurpation.

**État : décision documentaire adoptée, implémentation non commencée.** Voir le [statut du projet](status.md) et les [modules](../04-modules/README.md).
