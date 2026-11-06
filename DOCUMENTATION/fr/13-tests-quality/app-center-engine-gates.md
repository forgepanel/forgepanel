<!-- forgepanel-doc id=FP-13-APP-CENTER revision=3 status=specified -->
# App Center — matrice de qualification native vs conteneurs

[English](../../en/13-tests-quality/app-center-engine-gates.md) · [QA](README.md) · [Contrat App Center](../06-apps-recipes/app-center-engines.md)

**Tous les tests suivants sont PLANNED, jamais PASS.** Aucun moteur d'applications natif ou Docker/Podman opérationnel n'est importé ou disponible dans le Core actuel. Les tests documentaires de classification ne prouvent pas un déploiement.

## ONE-CLICK INSTALL — tests natifs gratuits

| Test ID | Cas | Attendu |
|---|---|---|
| TEST-APP-NAT-0001 | Installer un WordPress natif dans un site autorisé avec PHP-FPM/SQL disponibles | Succès sans Docker/Podman, sans licence Hub ou paiement |
| TEST-APP-NAT-0002 | App installée sans Hub ou en mode hors ligne | Installation native gratuite toujours possible depuis catalogue local sûr |
| TEST-APP-NAT-0003 | Gestionnaire de site tente autre tenant/site | Refus indépendant de l'interface |
| TEST-APP-NAT-0004 | PHP/WebStack/extension incompatible ou version EOL non autorisée | Refus avant mutation ; explications |
| TEST-APP-NAT-0005 | Téléchargement d'archive altérée, source non fiable ou version non approuvée | Rejet d'intégrité et provenance |
| TEST-APP-NAT-0006 | Chemin contenant traversal/symlink vers autre site | Refus au niveau filesystem et opérations typées |
| TEST-APP-NAT-0007 | Collision DB, quota disque/inodes, ressources PHP | Plan d'impact puis refus sans effet partiel incohérent |
| TEST-APP-NAT-0008 | Requête dupliquée, panne pendant extraction/DB/configuration | Idempotence, statut durable et récupération |
| TEST-APP-NAT-0009 | Mise à jour avec migration DB partiellement irréversible | Backup cohérent et avertissement ; aucune fausse promesse de rollback |
| TEST-APP-NAT-0010 | Désinstallation avec fichiers/DB/sauvegardes | Choix explicite de rétention, audit, pas de suppression silencieuse |
| TEST-APP-NAT-0011 | Tentative d'injecter des commandes dans config ou permissions | Aucun shell générique, exécuteur à opérations bornées |
| TEST-APP-NAT-0012 | Une version/une app exigent une licence tierce | Informations de licence affichées ; moteur gratuit ≠ app commerciale gratuite |

## CONTAINER APPS — tests propres aux conteneurs

| Test ID | Cas | Attendu |
|---|---|---|
| TEST-APP-CTR-0001 | Absence de Docker/Podman installé | Aucune tentative implicite de conversion native ou installation de runtime |
| TEST-APP-CTR-0002 | Pilote Docker disponible et manifest compatible | Déploiement seulement sous politique et ressources vérifiées |
| TEST-APP-CTR-0003 | Pilote Podman disponible mais Compose Docker non qualifié | Refus, aucune présomption de compatibilité |
| TEST-APP-CTR-0004 | Image inconnue, mutable ou signature/pin requis manquant | Refus de publication/de déploiement selon politique |
| TEST-APP-CTR-0005 | Montage `/` ou socket Docker, mode privileged, host network, provider, include ou références externes non autorisées | Bloqué par défaut ; pas de contournement via Compose |
| TEST-APP-CTR-0006 | Collision port avec FORGE 8447, PANEL 8446 ou site existant | Refus sans modifier les listeners |
| TEST-APP-CTR-0007 | Quotas CPU/RAM/PIDs/stockage/volumes insuffisants | Refus avant téléchargement/lancement ou compensation testée |
| TEST-APP-CTR-0008 | App multi-services : base, volumes et réseau | Dépendances, secrets, ordre et health checks réellement vérifiés |
| TEST-APP-CTR-0009 | Client natif demande action sur conteneur sans scope | Refus RBAC/agent, même avec accès à App Center |
| TEST-APP-CTR-0010 | Upgrade d'image avec migration persistante en erreur | Volume conservé et procédure de récupération explicite |
| TEST-APP-CTR-0011 | Retrait d'une app avec conteneurs et volumes | Choix distinct de conservation des volumes/données/backups |
| TEST-APP-CTR-0012 | Coupure réseau, manque d'espace image ou démarrage partiel | État observé, reprise/idempotence, jamais faux SUCCEEDED |

## Tests transversaux

| Test ID | Cas | Attendu |
|---|---|---|
| TEST-APP-X-0001 | Même logiciel avec recettes native et conteneur | Fiches, prérequis, identités d'installation et upgrades distincts |
| TEST-APP-X-0002 | Requête native portant un manifest `container_stack`, ou inversement | Rejet de type avant allocation de ressources |
| TEST-APP-X-0003 | Installation, suppression ou accès local quand Hub absent | Core libre et données clients fonctionnels, sans entitlement |
| TEST-APP-X-0004 | Catalogue officiel/partenaire non approuvé, signature invalide | Rien d'exécutable, même si fiche affichable en brouillon |
| TEST-APP-X-0005 | Ressource passée de site natif à app conteneur automatiquement | Refus sans workflow de migration dédiée |
| TEST-APP-X-0006 | Logs, diagnostics et événements d'échec avec secrets | Secrets masqués ; audit tenant/acteur/job/digest |
| TEST-APP-X-0007 | Projet 1Panel ou Softaculous copiés sans preuve de licence | Refus de publication tant que provenance et licences non validées |
| TEST-APP-X-0008 | Catalogue local vide ou moteur indisponible | UI expose l'état clairement ; autres services Core non affectés |

## Preuves de validation

Pour déclarer `VERIFIED`, lier chaque test au commit exact, OS/version, WebStack/PHP ou version Docker/Podman, manifeste et digest, tenant/permissions, ressources mesurées, résultat et reprise après échec. Tests positifs **et** négatifs sur VM réelle, notamment isolation multi-tenant. Les tests documentaires ne valent pas certification ni validation d'un moteur.

Les choix Q1–Q170 restent actifs. Les nouveaux mécanismes et la priorisation précise sont soumis aux revues spécialisées, sans attribuer des PASS fictifs.
