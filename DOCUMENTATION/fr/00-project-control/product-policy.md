<!-- forgepanel-doc id=FP-00-POLICY revision=3 status=documented -->
# Décisions produit du 5 novembre 2026 — gratuit, commercial et configurable

[English](../../en/00-project-control/product-policy.md) · [Registre ADR](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## Décisions du propriétaire (confirmées, mais pas implémentées)

| Référence | Décision | Portée et invariants |
|---|---|---|
| Q1, Q48 | **AGPL-3.0 + licence commerciale** | Double licence confirmée ; variante AGPL only/or-later, détenteurs de droits et texte commercial à valider avant d'ajouter LICENSE. |
| Q2, Q50 | **Core complet gratuit + plugins spécialisés, services cloud/managés, partenaires et support payants** | L'installation, l'hébergement essentiel et la récupération ne dépendent d'aucun achat, licence commerciale ou Hub. |
| Q3, Q54 | **Hébergement mutualisé + VPS en premier** | Développeurs/conteneurs et revendeurs ensuite, par jalons et tests vérifiés. |
| Q4, Q51 | PHP, Node.js, Python et **Docker + Podman** | Deux pilotes indépendants avec choix compatible par hôte ; runtimes clients distincts de Symfony, et Python toujours optionnel pour l'automatisation. |
| Q5, Q55 | **Une marque par organisation** | Logo, thème, domaine/HTTPS, messages et portail configurables pour cette identité unique ; aucune multimarque interne à l'organisation. |
| Q6 | Enregistrement et contact Hub avec consentements séparés | Installation standard autonome ; gestion explicite des canaux enregistrement, droits premium, vérification de versions, statistiques limitées, diagnostics/support et communications. Pas de collecte implicite des données d'hébergement. |
| Q7, Q52 | **60 jours**, puis nouvelles opérations premium bloquées et existant conservé | Droits premium précédemment vérifiés dans leurs limites contractuelles ; aucune suppression ni interruption du Core gratuit. Règles d'expiration/révocation explicite à préciser. |
| Q8, Q53 | **Officiels + candidature de partenaires et vérification manuelle** | Aucune publication directe sans approbation, même après envoi de candidature ; signature et revue par version requises. |
| Q47 | Changement sensible avec plan/validation/sauvegarde/récupération | Exposer impact, test de configuration, sauvegarde avant modification, vérification post-application et compensation/récupération quand possible. Un rollback universel SQL/OS n'est pas promis. |

Ces décisions s'ajoutent à ADR-013 : **MFA administrateur facultatif**, proposé sans bloquer le premier setup. Un choix commercial ou de présentation ne peut jamais contourner l'autorisation locale ni les droits Linux.

## Protection du produit et des abonnements

Le propriétaire souhaite protéger les modules payants et les abonnements. Le Hub pourra contrôler les achats, l'accès aux téléchargements autorisés, les renouvellements, les services hébergés et les droits de mise à jour des produits premium **juridiquement indépendants**. Un code AGPL déjà diffusé ne peut être soumis à une redevance obligatoire pour exercer ses droits. Une licence commerciale alternative ne supprime pas les libertés des copies reçues sous AGPL ; l'indépendance des plugins fermés doit être évaluée. Voir la [spécification de licence et commerce](license-commerce.md).

## Séparation Core gratuit / services commerciaux

Le Core couvre l'installation, le compte administrateur, la gestion des comptes et sites, l'isolation, les domaines, le SSL, l'accès aux fichiers, l'administration des services natifs retenus, les quotas, sauvegardes et récupération. La liste exacte de fonctionnalités minimales de la release reste à établir par critères d'acceptation.

Les offres premium peuvent porter sur des extensions non essentielles, services managés, support prioritaire, offres partenaires, hébergement de catalogue ou outils spécialisés. Une fonctionnalité de sécurité déjà nécessaire au Core ne devient pas payante par renommage. La facturation et les droits commerciaux appartiennent au Hub, pas au chemin de démarrage ou de récupération du Core.

## Politique des 60 jours — spécification de principe

Le Hub peut émettre des preuves de droits vérifiables localement. Le client conserve la dernière preuve authentique connue ; une panne réseau place le droit en état `offline-grace` pour **au plus 60 jours depuis la dernière vérification positive**, sans dépasser une échéance contractuelle explicitement opposable. Le comportement à expiration commerciale, révocation, changement d'horloge ou absence de première validation doit être précisé avant implémentation. Aucune commande distante ne doit arrêter les sites clients. Ce délai concerne les droits optionnels, jamais la capacité d'utiliser le Core complet gratuit.

## Personnalisation et permissions

Les choix UI peuvent être surchargés par organisation dans les limites de la politique du serveur. Les réglages sensibles nécessitent autorisations effectives et traçabilité : une permission de white-label ne donne pas accès aux clés de certificats privées ou aux comptes clients étrangers. Les utilisateurs peuvent consulter les valeurs héritées et pourquoi certaines options sont verrouillées.

## Décisions Q56–Q60 confirmées

Q56 **C** — paiements multi-prestataires via pilotes indépendants ; Q57 **C** — canaux Stable/Beta/Dev, déploiement progressif et retour arrière contrôlé ; Q58 **C** — comptes locaux et SSO/OIDC facultatif ; Q59 **C** — conservation configurable selon la catégorie sous limites légales et de sécurité ; Q60 **C** — achat définitif, abonnement, essais, coupons, packs et options.

Le Core demeure complet et gratuit. Les paiements/offres appartiennent au Hub, tandis que la vérification et l'exécution locales des mises à jour relèvent du Core. Aucun fournisseur, pourcentage de diffusion, nombre de jours de conservation ou politique de mises à jour automatiques n'a encore été choisi. Le détail des interfaces et tests figure dans [Q56–Q60](commerce-identity-release-policy.md).

## Décisions Q61–Q70 confirmées

L'éditeur a validé les dix choix Q61 C, Q62 C, Q63 C, Q64 C, Q65 D, Q66 C, Q67 D, Q68 C, Q69 D, Q70 D. Ils prévoient publication signée et installateur universel, services DNS/mail modulaires, sauvegardes avec réplication/immutabilité, approbations sensibles, orchestration et HA, monitoring externe, frontaux multiples et édition visuelle. La marque demeure **unique par organisation** (Q55) et le MFA administrateur reste **facultatif**. La haute disponibilité et les fonctions avancées se déploient par phases, sans contraindre la première version. [Exigences Q61–Q70](infrastructure-decisions.md).

## Questions encore ouvertes — ne pas présumer

Q48–Q55 sont **décidées** (voir tableau). Sujets ouverts : AGPL `only` ou `or-later` et licence commerciale, texte CLA et détenteur de droits, conditions de commercialisation de chaque module, moteur par défaut par OS et confinement, expirations/révocations distinctes de la simple perte de réseau, liste des critères partenaires, calendrier exact des jalons et validation des domaines de la marque unique. Les modalités opérationnelles de Q56–Q70 (fournisseurs, politiques exactes, sécurité et exploitation) restent à concevoir et tester.

**État : décision documentaire adoptée, implémentation non commencée.** Voir le [statut du projet](status.md) et les [modules](../04-modules/README.md).
