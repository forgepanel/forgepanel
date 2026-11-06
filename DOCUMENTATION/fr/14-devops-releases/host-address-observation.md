<!-- forgepanel-doc id=FP-14-HOST-OBSERVE revision=2 status=specified -->
# Observation IP et DNS local facultatif — préparation R3 indépendante

[English](../../en/14-devops-releases/host-address-observation.md) · [DevOps](README.md) · [Outils](../../../tools/host-address-observation/README.md)

## État et limites

Le module Go autonome [tools/host-address-observation](../../../tools/host-address-observation/README.md) comporte deux commandes distinctes. **`forgepanel-host-observe`** recense les interfaces/adresses IP et le FQDN candidat de l'OS sans réseau. **`forgepanel-dns-observe --observe`** effectue une unique interrogation A/AAAA, facultative et limitée, par le résolveur système, uniquement pour le nom candidat détecté. Cette seconde commande peut générer du trafic DNS ; elle n'est jamais exécutée implicitement. Aucun nom de domaine libre en argument, shell root, modification du système ou service externe de recherche d'IP publique. Ces commandes restent des prototypes de préparation, sans intégration Core ni certification HTTPS/OS.

Les chemins/ports fixes choisis sont **FORGE `/forge:8447`** et **PANEL `/panel:8446`**. Aucun champ domaine personnalisable ni virtual host automatique sur 443. Un même FQDN vérifié pourrait ultérieurement desservir les deux ports, **sans que ce prototype le démontre**.

## Interprétation et sécurité

- L'inventaire OS filtre, trie, déduplique et limite les adresses des interfaces actives. Une adresse non privée **n'est pas nécessairement publique ni joignable** derrière NAT/pare-feu.
- Le FQDN syntaxiquement valide de l'OS n'est que `CANDIDATE_UNVERIFIED`. Aucun FQDN => `NO_FQDN` et **aucune** requête DNS.
- La commande facultative rapporte `MATCHED_LOCAL_OS_RESOLVER_ONLY` lorsque toutes les réponses acceptées correspondent aux IP locales ; une différence devient `NAT_OR_REMOTE_ROUTING_UNVERIFIED`. Les deux statuts restent **non vérifiés**. Le résolveur peut lire `/etc/hosts`, du cache ou du DNS privé.
- Interrogation limitée en durée et en nombre de réponses ; refus des IP loopback/non adaptées, normalisation IPv4/IPv6 et remplacement des erreurs brutes par des codes d'avertissement sans secrets.
- Le rapport conserve toujours `dns_authority_verified=false`, `public_reachability=NOT_EXECUTED`, `tls_verification=NOT_EXECUTED`, `listener_verification=NOT_EXECUTED` et `verified_access_urls=[]`.
- Aucun contrôle de certificat IP-SAN/FQDN SAN, de DNS indépendant externe, d'accès HTTPS réel sur 8447/8446 ni génération d'URL fonctionnelle n'est effectué.

## Tests et prérequis

La [CI dédiée](../../../.github/workflows/host-address-observation.yml) lance les tests Go hors ligne, le détecteur de concurrence, `go vet`, le refus de produire des URL vérifiées et l'obligation du paramètre explicite de requête DNS. Les faux résolveurs des tests ne font aucune requête réseau. L'intégration Core exige encore l'import source #2, Symfony/PostgreSQL #3, l'installateur et les revues de sécurité ; l'[issue #51](https://github.com/yyogas/forgepanel/issues/51) couvre la validation DNS/TLS/proxy/cookies/VM réelle. Ce prototype ne doit pas être décrit comme un Core installé.

**État : code source autonome candidat seulement ; aucun domaine, endpoint HTTPS ou accès public certifié, ni déploiement Core.**
