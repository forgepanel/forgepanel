<!-- forgepanel-doc id=FP-16 revision=1 status=documented -->
# Performance et capacité

[English](../../en/16-performance/README.md) · [Index](../README.md)

Les éléments inspectés n'établissent aucun benchmark représentatif ForgePanel, capacité d'hébergement ou objectif de service en production. Ne pas classer les stacks par une vitesse universelle non mesurée. La durée des tests natifs n'est pas un benchmark.

## Plan de mesure

Mesurer latence interactive du panneau (p50/p95/p99 et erreurs), nombre/durée des requêtes SQL, mémoire par worker, attente/exécution des jobs, impact des reloads et isolation sous concurrence. Fixer charge, données, matériel, OS, runtime, commit et état des caches. Séparer démarrage froid/chaud, répéter les essais et garder les résultats bruts expurgés. Définir les seuils après état de référence et cible produit, pas par invention ici.

Tester le panneau séparément du trafic client, puis ensemble sous contention. Inclure tâches longues, annulation, erreurs et dépendance indisponible ; les seules réussites masquent la surcharge. Une sélection d'OS sur fixtures ne mesure ni noyau, ni système de fichiers, ni serveur web.

## Contraintes d'optimisation

Sortir les opérations système lourdes des requêtes HTTP. Privilégier index ciblés et requêtes bornées avant les caches distribués. Redis reste facultatif jusqu'à justification mesurée. OPcache et pools nécessitent validation par environnement ; le bénéfice du JIT n'est pas présumé. Ne pas partager le cache des pages privées entre identités ni conserver des autorisations périmées. Éviter les rafraîchissements Live Components complets à haute fréquence pour la télémétrie ; mesurer les limites du transport UI.

Tout changement de runtime, mode worker ou profil web comprend tests de correction/isolation et résultats de performance. Un gain de débit ne justifie ni contournement `.htaccess`, ni suppression des quotas, ni moindre protection des secrets. Budgets de régression et tests de charge reproductibles appartiennent au futur jalon d'intégration.

[Architecture](../02-architecture/README.md) · [Exploitation](../15-operations/README.md)
