<!-- forgepanel-doc id=FP-14-HOST-OBSERVE revision=1 status=specified -->
# Observation autonome des adresses de la machine — outil préparatoire R3

[English](../../en/14-devops-releases/host-address-observation.md) · [DevOps](README.md) · [PR #50 — Contrat des portails](https://github.com/yyogas/forgepanel/pull/50)

## Provenance et état

L'outil Go dans [tools/host-address-observation](../../../tools/host-address-observation/README.md) constitue un **PROTOTYPE IMPLÉMENTÉ autonome**, pas l'import des sources historiques Foundation v0.7 ni un composant Core opérationnel. Il s'exécute sans privilège root, appel réseau, interrogation DNS, shell, socket en écoute, écriture fichier ou modification du système. **L'import R1 et l'intégration Symfony/PostgreSQL R2 restent des prérequis indépendants.**

Les chemins et ports confirmés FORGE (/forge, HTTPS 8447) et PANEL (/panel, HTTPS 8446) figurent dans le rapport comme **métadonnées fixes**, pas comme listeners installés. Le système d'exploitation fournit les IPv4/IPv6 et un éventuel nom complet candidat valide ; aucun domaine du portail personnalisable, sous-domaine forge./panel. ni hôte automatique 443. Les domaines des sites clients et le branding Q5 sont des fonctions distinctes.

## Interprétation du rapport

- Interfaces réseau : adresses unicast attribuées aux interfaces actives non-loopback, triées et dédupliquées ; états PRIVATE_UNVERIFIED ou NON_PRIVATE_UNVERIFIED. Ce dernier ne prouve **aucune IP publique ou routable**, notamment en présence de CGNAT ou de plages réservées.
- Nom de machine : un hostname complet de syntaxe valide devient CANDIDATE_UNVERIFIED ; un nom local incomplet est NONE. Aucune preuve A/AAAA n'est faite : /etc/hosts, caches DNS ou split-horizon ne suffisent pas.
- Vérification : DNS, TLS, listener et accessibilité publique restent NOT_EXECUTED ; verified_access_urls reste toujours vide. Une URL HTTPS par IP impose un certificat couvrant cette IP ; une URL domaine impose une validation DNS, routage et TLS préalable à tout affichage comme accès fonctionnel.
- Erreurs : lecture indisponible ou inventaire limité signalés UNAVAILABLE ou PARTIAL_UNVERIFIED avec avertissements assainis ; aucune adresse supposée ou faux succès.

## Tests et frontière d'intégration

La CI dédiée contrôle les tests Go sur interfaces simulées, le détecteur de courses, vet et l'absence de liens prétendument vérifiés. Ces vérifications concernent uniquement le **code autonome**. L'intégration [issue #51](https://github.com/yyogas/forgepanel/issues/51) exige encore l'import Foundation, les routes Symfony authentifiées, un contrat d'agent Go audité, des sondes DNS/TLS fiables, la vérification NAT et les essais HTTP/VM. Aucune API shell privilégiée ni dépendance au Hub éditeur n'est introduite.

**État :** code d'observation non privilégié testé localement ; intégration, vérification DNS/TLS, détection d'IP publique et URLs fonctionnelles restent NON IMPLÉMENTÉES.
