<!-- forgepanel-doc id=FP-00-LICENSE revision=1 status=specified -->
# Double licence AGPL-3.0 / commerciale et protection des offres

[English](../../en/00-project-control/license-commerce.md) · [Décisions](decisions.md) · [Politique produit](product-policy.md)

## Décisions confirmées — 2026-11-05

- **Q48 A** : modèle **GNU AGPL-3.0 + licence commerciale** pour le Core ForgePanel. La désignation finale `AGPL-3.0-only` ou `AGPL-3.0-or-later`, les textes commerciaux et les notices par fichier restent à valider avant de publier une licence exécutoire ; aucun `LICENSE` n'est encore installé.
- **Q49 A** : contributions acceptées via un **Contributor License Agreement (CLA)** donnant à l'éditeur les droits appropriés de diffuser/relicencier sous les deux licences, tout en permettant aux auteurs de conserver les droits définis par le CLA. Texte/identité juridique, consentement, processus de signature, règles pour mineurs/entreprises et politique de DCO restent à préparer et faire examiner.
- **Q50 B** : Core complet gratuit, **modules spécialisés**, services cloud/managés, offres partenaires et support commercial facultatifs. Ni le Core libre, ni le bootstrap, ni la réparation, ni l'hébergement essentiel ne dépendent d'un abonnement.
- **Précision du propriétaire** : « protéger notre produit sauf si [le client] paie module et abonnement ». Interprétation retenue **uniquement pour les produits commerciaux séparés** : téléchargements premium, abonnements et accès aux services d'éditeur exigent des droits contractuels valides, vérifiés par le Hub. Cette intention **n'autorise pas** à restreindre des copies ou des usages licites du Core AGPL.

## Libertés AGPL et limites de la monétisation

Les destinataires d'une copie sous AGPL disposent des libertés de l'utiliser, étudier, modifier et redistribuer selon la licence. L'éditeur peut **vendre** des licences alternatives, l'accès initial à certains canaux, du support et des services, mais ne peut pas ajouter à l'AGPL une obligation de paiement ou de télémétrie pour conserver l'usage/redistribution d'une copie déjà obtenue légitimement. Les versions modifiées accessibles par réseau déclenchent des obligations de fourniture de la source correspondante aux utilisateurs concernés selon l'AGPL.

Une même portion de code peut être distribuée par l'ayant droit sous deux licences ; cela suppose un inventaire des droits sur les contributions, les dépendances et les œuvres dérivées. **Le seul fait qu'un plugin soit dans un dépôt/processus séparé ne prouve pas sa compatibilité avec une licence propriétaire.** Une analyse de couplage réelle et juridique est exigée avant la distribution d'un module premium fermé.

## Ce qui peut être protégé commercialement

| Actif | Protection ciblée | Limite |
|---|---|---|
| Core ForgePanel | Copyright, obligations AGPL, offre de licence commerciale alternative, provenance et qualité | Pas de redevance obligatoire pour exercer les droits AGPL |
| Nom et logo | Politique de marque, usage de signes et identité officielle ; dépôt de marque à étudier | Les licences de code et marques sont distinctes |
| Paquets premium indépendants | Distribution autorisée, contrôle d'achat/abonnement, signature et garanties de mise à jour | Licence et séparation effective à vérifier avant diffusion |
| Services Hub/cloud/support | Authentification, paiement vérifié, abonnements, accès API et quotas de services | Un arrêt commercial ne doit pas couper les sites du Core |
| Chaîne de publication | Clés d'éditeur hors du code, signatures, contrôle des partenaires, révocation des artefacts compromis | Signature ne garantit pas la sécurité du logiciel |
| Installations clientes | Vérification des droits **premium seulement** ; 60 jours hors ligne pour les droits éligibles | Aucune API de télémétrie obligatoire ni commande de destruction |

## Conventions de contribution et provenance à établir

Le futur CLA doit indiquer l'éditeur/entité juridique, les droits de copyright/brevet accordés, la possibilité explicite de double licence et la validité des contributions de tiers. Enregistrer la preuve d'accord de chaque contributeur avant fusion commerciale. Auditer les licences des dépendances et séparer les éléments qui ne peuvent légalement être vendus en licence alternative sans consentement. Ne pas présumer que toutes les contributions sont éligibles automatiquement.

## Statuts et arbitrages restants

**CONFIRMÉ** : choix AGPL-3.0 + commercial, CLA, Core complet gratuit, premiums/services/support. **NON DÉCIDÉ** : version AGPL only/or-later, conditions de licence commerciale, architecture et licence précises des modules fermés, détenteur de marque et politique contractuelle de l'abonnement. **NON IMPLÉMENTÉ** : licences, serveur de droits, contrats et écosystème premium dans le Core.

Références juridiques de cadrage : [GNU FAQ](https://www.gnu.org/licenses/gpl-faq.fr.html), [GNU AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html) et [analyse des CLA](https://interoperable-europe.ec.europa.eu/collection/eupl/licences-complementary-agreements). Il s'agit d'une spécification produit, pas d'un avis juridique.
