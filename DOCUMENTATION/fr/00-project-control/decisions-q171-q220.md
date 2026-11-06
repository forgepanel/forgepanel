<!-- forgepanel-doc id=FP-00-Q171-220 revision=1 status=specified -->
# Q171–Q220 — registre des arbitrages produit approuvés

[English](../../en/00-project-control/decisions-q171-q220.md) · [Q161–Q170](decisions-q161-q170.md) · [App Center](../06-apps-recipes/app-center-engines.md) · [Réconciliation](reconciliation-q171-q220.md)

**APPROUVÉ PAR LE PROPRIÉTAIRE le 6 novembre 2026 : les 50 recommandations sont explicitement adoptées.** Q1–Q170 restent actifs ; aucune question sans réponse n'est supposée validée. Répartition : **47 D et 3 C (Q174, Q194, Q200)**. Ces orientations produit sont **SPECIFIED** et ne sont ni du code implémenté, ni une fusion, ni des tests de runtime, ni une release/déploiement. Le [registre machine](../../evidence/decisions-q171-q220-v1.json) réplique les choix. Prix, fournisseurs, valeurs par défaut et calendrier restent OUVERTS.

| ID | Choix | Orientation produit approuvée | Périmètre |
|---|---|---|---|
| Q171 | **D** | Catalogue natif extensible par catégories, démarrage progressif des recettes qualifiées | Core + métadonnées/édition Hub |
| Q172 | **D** | API de provisioning versionnée, opérations prédéfinies, RBAC et audit, connecteurs indépendants | Core + métadonnées/édition Hub |
| Q173 | **D** | Architecture antivirus multiscanner, jobs bornés, quarantaine réversible, politique et audit | Core local |
| Q174 | **C** | Pilote WAF candidat Coraza + OWASP CRS, mode détection puis blocage après qualification | Core local |
| Q175 | **D** | FORGE/PANEL strictement séparés : sessions, routes, API, thèmes, menus et permissions ; Hub isolé | Core local |
| Q176 | **D** | Après socle hébergement R4, One-Click natif puis conteneurs par jalons de qualification indépendants | Core local |
| Q177 | **D** | Catégories applicatives administrables avec compatibilités et éligibilité vérifiées | Core + métadonnées/édition Hub |
| Q178 | **D** | Recettes officielles, partenaires approuvés et import local signé soumis à revue préalable | Core + métadonnées/édition Hub |
| Q179 | **D** | Modes simple/avancé, préflight, estimation, backup, aperçu et modèles administrables | Core local |
| Q180 | **D** | Configuration héritée global → serveur → organisation → plan → site, limitée et historisée | Core + métadonnées/édition Hub |
| Q181 | **D** | Moteur SQL recommandé selon compatibilité de chaque application ; choix, droits et quotas contrôlés | Core local |
| Q182 | **D** | Versions applicatives certifiées, gel, EOL, politiques et migrations par application/site | Core + métadonnées/édition Hub |
| Q183 | **D** | Mises à jour configurables par app/site avec fenêtre, staging, sauvegarde et approbation | Core + métadonnées/édition Hub |
| Q184 | **D** | Sauvegarde fichiers et SQL cohérente, contrôle de restauration et avertissements sur irréversibilité | Core local |
| Q185 | **D** | Désinstallation avec choix de conservation selon tenant/site, confirmation et audit | Core local |
| Q186 | **D** | Détection et adoption d'apps existantes en lecture seule d'abord, puis revue/autorisation | Core local |
| Q187 | **D** | Installations en masse gouvernées par concurrence, quotas, annulation et reprise | Core local |
| Q188 | **D** | Staging isolé, données masquées, secrets distincts, mail/webhooks externes désactivés par défaut | Core local |
| Q189 | **D** | Secrets applicatifs gérés par pilotes, périmètre site, rotation, accès bornés et audit | Core local |
| Q190 | **D** | RBAC délégable par opération, site, organisation et plan, sous politique serveur | Core local |
| Q191 | **D** | Activation conteneurs seulement sur serveur qualifié et selon droits du plan/organisation | Core local |
| Q192 | **D** | Pilotes Docker/Podman indépendants, sélection après compatibilité certifiée app/hôte | Core + métadonnées/édition Hub |
| Q193 | **D** | Rootless préféré, exceptions approuvées, profils d'isolation et audits par classe | Core local |
| Q194 | **C** | Compose uniquement via recettes et fournisseurs précisément qualifiés, aucun fichier arbitraire | Core + métadonnées/édition Hub |
| Q195 | **D** | Images par digest/signature et registres autorisés, retraits et versions compatibles | Core + métadonnées/édition Hub |
| Q196 | **D** | Capabilities minimales, rejet par défaut privileged, sockets moteurs et montages sensibles | Core local |
| Q197 | **D** | Réseaux conteneurs segmentés, politiques entrantes/sortantes, ports et exposition configurés | Core local |
| Q198 | **D** | Volumes persistants sous quotas, sauvegardes, rétention, chiffrement et vraie restauration | Core local |
| Q199 | **D** | Budget CPU/RAM/PIDs/I/O/stockage par hôte, plan, tenant et app, plafonné physiquement | Core local |
| Q200 | **C** | Migration native↔conteneurs via assistant explicite export/import, sauvegarde et validation | Core + métadonnées/édition Hub |
| Q201 | **D** | Catalogues signés, cache, clés rotatives, anti-rollback, provenance et retrait | Core + métadonnées/édition Hub |
| Q202 | **D** | Éditeurs et versions partenaires vérifiés : sécurité, maintenance, licences, retrait | Core + métadonnées/édition Hub |
| Q203 | **D** | Suivi des vulnérabilités des versions installées, politiques de risque et remédiations approuvées | Core + métadonnées/édition Hub |
| Q204 | **D** | Réponse graduée aux recettes dangereuses : empêcher nouvelles poses, alerter, préserver données | Core + métadonnées/édition Hub |
| Q205 | **D** | Quarantaine malware réversible, contrôles de faux positifs et règles/approbations par site | Core local |
| Q206 | **D** | WAF à politiques héritées, simulation, détection puis blocage qualifié et rollback | Core local |
| Q207 | **D** | Journaux structurés et expurgés, corrélation, RBAC, filtres, rétention et export | Core + métadonnées/édition Hub |
| Q208 | **D** | Réauthentification/approbation selon risque, opération, ressource et devoir de séparation | Core + métadonnées/édition Hub |
| Q209 | **D** | Préflight, réservation atomique, revalidation à l'effet, idempotence et reprise | Core local |
| Q210 | **D** | Sources d'artefacts contrôlées, cache signé, validation SSRF et reprise vérifiée | Core + métadonnées/édition Hub |
| Q211 | **D** | Deux espaces App Center distincts avec recherche commune en lecture seule et compatibilité | Core + métadonnées/édition Hub |
| Q212 | **D** | Distinguer moteur natif gratuit, licence/coût tiers, ressources et offres optionnelles | Core + métadonnées/édition Hub |
| Q213 | **D** | Catalogue local sûr/versionné hors ligne, synchronisations signées facultatives, Hub non requis | Core + métadonnées/édition Hub |
| Q214 | **D** | Droits revendeur par tenant/plan/catégorie/moteur bornés par politique serveur | Core local |
| Q215 | **D** | Classement d'abord compatibilité/sécurité puis filtres/stats ; sponsor identifié si activé | Core + métadonnées/édition Hub |
| Q216 | **D** | Intégrations de facturation par API stable et connecteurs indépendants qualifiés | Core + métadonnées/édition Hub |
| Q217 | **D** | Webhooks/événements versionnés et signés, idempotents, filtrés, destinations approuvées | Core + métadonnées/édition Hub |
| Q218 | **D** | API publique progressive d'opérations prédéfinies, scopes, RBAC, limitation de débit et audit | Core local |
| Q219 | **D** | Observabilité par moteur : logs, métriques, santé, événements, quotas, seuils et diagnostics | Core + métadonnées/édition Hub |
| Q220 | **D** | Configuration Center versionné, héritage, règles, simulation, RBAC, historique et récupération | Core + métadonnées/édition Hub |


## Interprétation et limites obligatoires

- **Q171/Q176 et R1–R4/Q119/Q120** : un grand catalogue natif est une **cible progressive**, pas vingt apps obligatoires dès la première version. Le premier site PHP/HTTPS et le véritable Symfony/PostgreSQL restent préalables ; les conteneurs suivent des pilotes indépendamment qualifiés (Q51).
- **Q172/Q216/Q218** : un ensemble cohérent d'API versionnées **typées et bornées** pour provisioning/facturation/actions publiques, avec connecteurs indépendants. Jamais trois systèmes contradictoires ni une API générique shell/root. Idempotence et permissions tenant/site requises.
- **Q173/Q205 et Q174/Q206** : antivirus et WAF sont complémentaires. **Q174 C** retient Coraza + OWASP CRS comme **intégration WAF candidate, détection d'abord**, pas un blocage imposé à tous les sites sans qualification. Moteurs scanner, seuils et compatibilités restent ouverts.
- **Q175/Q5/Q55/ADR-008** : FORGE `/forge:8447` et PANEL `/panel:8446` conservent sessions et thèmes séparés. La directive récente de **détection IP machine/FQDN existant vérifié** vise les **accès des portails système**, **sans domaine système personnalisé** dans l'installateur ; le white-label à une marque par organisation et les **domaines des sites hébergés** sont distincts. Les anciennes mentions d'hôtes système configurables devront être réconciliées de manière ciblée.
- **Q178/Q202 et Q8/Q53/Q114** : import local signé et partenaires exigent **revue manuelle explicite par version**, provenance, licence et autorisation. Aucun catalogue auto-publié non vérifié ; aucune licence de code tiers n'est transférée automatiquement.
- **Q180/Q220/Q190/Q214** : héritage des réglages et délégation revendeur ne contournent ni autorisation, ni isolation, ni plafonds physiques. Les revendeurs restent une phase ultérieure et ne deviennent pas implémentés par ce vote.
- **Q183/Q184/Q185/Q200** : mises à jour, migrations SQL et transfert natif↔conteneur exigent plan, backup, validation, rétention et récupération. **Q200 C = assistant export/import contrôlé, pas la conversion automatique de l'option D** ; aucun rollback SQL universel.
- **Q193/Q194/Q195/Q196/Q197** : rootless favorisé selon certification OS/pilote. **Q194 C n'approuve que Compose/recettes/fournisseurs qualifiés, pas l'éditeur avancé de stacks de l'option D**. Refus par défaut des mounts dangereux, sockets moteur et exécution privilégiée.
- **Q201/Q203/Q204/Q210** : catalogues signés et réponse aux risques n'autorisent aucune suppression destructive, source non fiable ou contrôle Linux par le Hub. Core autonome sans Hub.
- **Q207/Q219 et Q6/Q158/Q168** : logs et métriques locaux ne donnent aucun accord implicite de télémétrie Hub ; diagnostics externes soumis à consentement, minimisation, seuils de cohortes et rétention.
- **Q208 avec Q66/Q76/Q163** : réauthentification, approbations, exception limitée aux budgets de performance non critiques et secours audité demeurent ; **MFA toujours facultative**, sans dérogation aux veto sécurité/backup/QA.
- **Q211/Q212/Q213/Q215** : deux espaces distincts, recherche commune en lecture seule et sponsor facultatif clairement indiqué ; rien ne bloque l'installateur natif gratuit ni le classement organique basé sur la compatibilité.

## Détails et preuves encore ouverts

Ces orientations **ne fixent pas** les moteurs antivirus définitifs, les clés de signature, versions WAF, pilotes Docker/Podman par défaut, payloads API, tables PostgreSQL, seuils sécurité, prix, applications, durées de rétention, mises à jour automatiques par défaut, exposition réseau ou résultats de certification. Ces éléments attendent des arbitrages ou revues techniques spécialisées. Voir la [réconciliation et les handoffs](reconciliation-q171-q220.md). **Aucun code ni test d'intégration n'est approuvé par ce registre.**
