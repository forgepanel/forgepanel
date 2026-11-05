<!-- forgepanel-doc id=FP-00-STATUS revision=1 status=documented -->
# État et roadmap ordonnée par dépendances

[English](../../en/00-project-control/status.md) · [Pilotage](README.md)

## Niveaux de preuve

`PROPOSED` : option à examiner. `SPECIFIED` : exigences/contrats rédigés. `IMPLEMENTED` : code existant dont l'emplacement est précisé. `VERIFIED` : vérification nommée exécutée sur une entrée et un environnement identifiés. `PUBLISHED` : release et artefacts identifiables. `DEPLOYED` : environnement et révision déployée identifiés. `MERGED` décrit seulement l'intégration Git. Le statut documentaire est distinct du statut fonctionnel.

## État initial au 2026-11-05

| Périmètre | État réel |
|---|---|
| GitHub avant ce lot | Privé, vide ; aucune branche, commit, issue, PR ou release retournée |
| Dépôt après ce lot documentaire | Documentation, gouvernance et validation documentaire ; aucun import applicatif |
| Foundation v0.6/v0.7 | Archives de développement fournies ; provenance enregistrée dans l'audit |
| Tests natifs v0.7 | Réexécutés avec succès dans le conteneur local ; pas de certification VM |
| Intégration HTTP Symfony et PostgreSQL | Sources/test fournis ; non exécutés dans cet audit |
| Installateur, agent complet, WebStacks, RBAC complet, plugins | Non disponibles comme produit fonctionnel |
| Release et production | Aucune preuve ; licence non décidée |

Les six OS et cinq profils sont des entrées de planification. Trente combinaisons de fixtures ne sont pas trente installations. La branche `production` pointe initialement vers un commit d'amorçage contenant uniquement un README et ne déploie rien.

## Roadmap

| Priorité | Livrable | Dépendance et preuves de sortie |
|---|---|---|
| P0 | Référence documentaire et PR relue | Contrôles liens/parité ; faits et risques consignés |
| P1 | Import du code avec provenance | Inventaire v0.7 revu ; aucun secret/binaire généré ; statut de licence explicite ; tests répétés sur le commit importé |
| P2 | Intégration Symfony + PostgreSQL | Résolution/verrouillage/audit des dépendances ; tests HTTP, rollback/concurrence SQL et navigateur réels |
| P3 | Identité permanente et récupération | Connexion/déconnexion, MFA facultatif (activation/désactivation/récupération), autorisation contextualisée, isolation des sessions ; corriger le setup v0.7 |
| P4 | Paquets et services sur six OS | Origines de paquets fiables, politique runtime, systemd et contrôles obligatoires validés en VM |
| P5 | Exécution des plans et installation en une commande | Étapes durables, reprises sûres, TLS, rollback/compensation, distribution signée et tests réinstallation/mise à jour |
| P6 | Modules d'hébergement et autres stacks | Isolation, limites, sauvegardes/restaurations et preuves VM par profil |
| P7 | Écosystème tiers | Modèle de confiance, contrats, isolation et maintenance validés avant exécution |

Ces priorités n'engagent aucune date ni version. Arbitrages produit nécessaires : licence du logiciel/des contributions et canal privé de sécurité autorisé. Les choix paquets/runtimes nécessitent une proposition technique étayée, pas une nouvelle architecture implicite.
