<!-- forgepanel-doc id=FP-00-CIRP revision=1 status=specified -->
# Décisions Q56–Q60 — Paiements, canaux, identité, conservation et offres

[English](../../en/00-project-control/commerce-identity-release-policy.md) · [Registre ADR](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## État et portée

Le 5 novembre 2026, le propriétaire a **confirmé Q56 C, Q57 C, Q58 C, Q59 C et Q60 C**. Il n'a **pas encore répondu à Q61–Q70**, qui restent ouverts. Il s'agit d'exigences de produit, **pas** de services opérationnels, d'une licence exécutoire ou d'une release. Le Core demeure AGPL-3.0 + commerciale en projet (textes exacts ouverts), complet et gratuit pour ses fonctions essentielles ; le Hub privé fournit les capacités commerciales facultatives.

## Décisions confirmées

| ID | Choix | Règle et composant responsable |
|---|---|---|
| Q56 C | Plusieurs prestataires de paiement via **pilotes indépendants** | `ForgePanel-Hub` possède les fournisseurs, les commandes et leurs callbacks ; aucune intégration/clé/fournisseur réel choisi. Pas de paiement demandé pour utiliser le Core libre. |
| Q57 C | Canaux **Stable, Beta, Dev**, déploiement progressif et retour arrière | Le Core vérifie localement signature, version, compatibilité et permission avant application ; le Hub peut publier métadonnées et politiques de campagnes. Une migration irréversible ne peut être annulée par simple retour du binaire. |
| Q58 C | **Comptes locaux + SSO/OIDC facultatif** | Le Core doit conserver une identité locale administrateur et un chemin de récupération contrôlé ; OIDC peut être activé séparément pour une organisation et/ou le personnel éditeur. MFA administrateur **facultatif** (décision antérieure inchangée). |
| Q59 C | **Durées de rétention configurables par catégorie**, dans les limites légales et de sécurité | Logs techniques, audits, sessions, métriques, diagnostics, paiements et données personnelles ont des politiques distinctes. Aucun nombre de jours global n'est décidé. |
| Q60 C | **Achat définitif + abonnements récurrents + essais, coupons, packs et options complémentaires** | Le Hub gère produits, offres, droits signés et facturation ; un paiement confirmé par événement serveur vérifié permet l'attribution idempotente des droits. Le terme « définitif » ne préjuge pas de la durée de mises à jour/support. |

## Configuration Engine : règles par domaine

### Paiement et offres (Hub uniquement)

Les pilotes de paiement doivent exposer des contrats normalisés pour : identification/capacités du prestataire, création d'une session de règlement, vérification de notifications signées, recherche de transactions, rapprochement, événements de remboursement et état d'abonnement. Les méthodes de capture/remboursement dépendent des capacités déclarées et de la permission de l'opérateur. Les secrets sont stockés séparément des paramètres publics. Aucun fournisseur n'est choisi par défaut.

Les offres doivent accepter : `purchase_kind` (achat définitif/abonnement/essai), SKU, devise, prix et version des conditions, durée et renouvellement, droits inclus, packs, options, coupons avec conditions/plafonds, audit et politique d'expiration. Les taxes, marchés géographiques, factures et remboursements nécessitent des décisions légales et techniques ultérieures. Ne pas attribuer de droits depuis une page de succès navigateur.

### Publication et mises à jour

Canaux `stable`, `beta`, `dev` (identifiants d'API proposés). Sélection par serveur/compte autorisé et compatibilité Core/OS/WebStack ; politiques de campagne progressive et groupes pilotes configurables. Tout déploiement doit utiliser métadonnées/artefacts vérifiés, sauvegarde et plan de récupération ; l'application locale est soumise au contrôle d'accès et au Configuration Engine. Les canaux Dev/Beta ne sont pas automatiquement recommandés à la production. La politique d'installation automatique et le taux de déploiement par défaut restent ouverts (Q61–Q70).

### Comptes et accès

Compte local utilisable sans fournisseur externe ; liaison optionnelle à un fournisseur OIDC après vérification de `issuer`, `audience`, intégrité des tokens et identités, scopes et groupes **ne constituant pas des privilèges par eux-mêmes**. Éviter les fusions de comptes par email seul. En panne IdP, la récupération locale reste maîtrisée, journalisée et protégée. L'administrateur peut choisir d'activer ou non le MFA. Les paramètres de sessions, confiance envers l'IdP, provisioning/déprovisioning et personnalisation par organisation restent à implémenter et tester.

### Conservation

Catégories proposées : audits de privilèges, logs système, télémétrie non sensible, jobs, sauvegardes, tickets, diagnostics consentis, identifiants de sessions et enregistrements commerciaux. Pour chaque catégorie : finalité, base légale ou exigence de sécurité, propriétaire, durée minimale/maximale autorisée, anonymisation, purge planifiée, archivage et preuve d'exécution. Une option administrative ne doit jamais autoriser une purge contraire à la loi, à un litige, aux exigences d'audit ou à la restauration. Les catégories commercialement conservées restent sous l'autorité du Hub.

## Invariants inter-projets

La communication Hub est facultative ou contractuellement limitée pour les services premium ; les consentements/enregistrements sont séparés (Q6). Aucun canal de mises à jour, IdP ni fournisseur de paiement ne doit empêcher le Core gratuit de démarrer, d'héberger ou de se réparer. Après 60 jours de grâce commerciale éligible, seules **les nouvelles opérations premium** sont refusées ; état et données restent conservés (Q52).

## Tests attendus, mais non exécutés

- Webhooks dupliqués/désordonnés, paiement confirmé après interruption, échec de fournisseur, coupon plafonné, essai expiré, droits attribués une seule fois.
- Canal incorrect/incompatible, signature invalide, déploiement en anneaux, version défectueuse, restauration de configuration, migration SQL non réversible.
- Identité SSO différente de l'identité locale, OIDC mal configuré, tentatives inter-organisations, perte de connexion à l'IdP et récupération locale sans escalade.
- Durées de rétention contradictoires, purge partielle, contraintes légales, restauration de backup, absence de secrets dans les logs.

## Arbitrages encore ouverts

Q61–Q70 : signatures et distribution, installation, DNS, mail, sauvegardes, contrôles sensibles, multi-serveurs, monitoring, WebStacks et design. En complément : prestataires réellement retenus, paramètres fiscaux, politique automatique de mises à jour, identité multi-tenant/OIDC, durées de conservation par type et distinction achat définitif/maintenance. Ne rien sélectionner implicitement.
