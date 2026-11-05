<!-- forgepanel-doc id=FP-10 revision=1 status=documented -->
# Modèle de sécurité et signalement

[English](../../en/10-security/README.md) · [Index](../README.md)

## Actifs, acteurs et frontières

Protéger privilèges Linux, données clientes, identifiants SQL, clés MFA/chiffrement, autorisations de setup, autorité de signature et intégrité de l'audit. Considérer appelants réseau anonymes, code client hostile, plugins compromis, entrées non fiables et interruptions privilégiées. Un processus déjà compromis comme utilisateur applicatif peut employer ses droits SQL ; le drapeau d'environnement bootstrap n'est pas une sandbox contre cet attaquant.

| Frontière | Exigence |
|---|---|
| Navigateur → Symfony | HTTPS vérifié, hôte/origine de confiance exacts, CSRF sur mutations, sessions sûres, limites d'essais, autorisation des ressources |
| Symfony → agent | Canal privé authentifié et versionné ; opérations typées autorisées ; aucune API `exec(command)` |
| Agent → Linux | Moindre privilège, exécuteur borné, chemins sûrs, verrous par ressource, audit système |
| Client → client | Identités/permissions distinctes et limites explicites ; un pool PHP-FPM seul ne suffit pas |
| Artefact → installation | Racine de confiance indépendante, signatures/empreintes vérifiées, anti-retour arrière et rotation sûre des clés |

SRC-03 n'implémente que les contrôles métier du setup et des protections HTTP dans les sources. Durcissement systemd, contrôles obligatoires, isolation client, rotation de secrets en production, connexion/RBAC complets et restauration ne sont pas démontrés.

## Critères minimaux de livraison

Ne jamais demander le mot de passe root Linux dans le panneau. Maintenir USER fermé avant validation des autorisations et sessions. Ne pas désactiver SELinux/AppArmor ou le pare-feu pour réussir un test. Éviter les secrets dans URL, logs et artefacts. Exiger diagnostic en lecture seule avant réparation proposée et autorisation explicite avant destruction. Les tests de restauration couvrent les clés, pas seulement SQL/fichiers.

Le verrouillage après cinq essais bootstrap peut servir au déni de service ; restrictions réseau et tests de récupération restent nécessaires. Des vecteurs TOTP validés ne constituent pas un audit cryptographique. Un port n'est pas une frontière d'autorisation.

## Signalement et revue

Aucune release de production supportée, adresse privée de signalement ou garantie de réponse n'est établie. Utiliser le signalement privé GitHub seulement s'il est disponible ; sinon demander un canal privé sans publier exploitation ou secrets. Établir ce canal avant distribution publique. La revue sensible doit être distincte de l'implémentation ; aucun relecteur indépendant n'était disponible pour cet audit documentaire. Voir le [registre des risques](../19-audits-risks/README.md).
