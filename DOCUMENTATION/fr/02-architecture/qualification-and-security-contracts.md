<!-- forgepanel-doc id=FP-02-Q151-160 revision=1 status=specified -->
# Qualification QEMU/KVM, sauvegardes testées et contrôles SFTP/bêta — Q151–Q160

[English](../../en/02-architecture/qualification-and-security-contracts.md) · [Décisions](../00-project-control/decisions-q151-q160.md) · [MVP](../00-project-control/mvp-qualification.md)

## Chaîne de preuve : Q151 A, Q152 C

Le premier adaptateur cible **QEMU/KVM local**, non un fournisseur cloud. `VmQualificationDriver` proposé : `preflightKvm()`, `createFromPinnedImage()`, `snapshot()`, `injectFailure()`, `restore()`, `collectReport()`, `destroy()`. Détecter KVM/nested virtualization et classer l'impossibilité d'exécution `SKIP/BLOCKED`, sans faux `PASS`. Le contrat multi-pilotes Q141 permet d'ajouter des VM cloud **plus tard**, sans recopier les tests.

`QualificationEvidence` proposé : référence OS/image immuable/empreinte, architecture, ressources VM, WebStack/profil, commit et artefact signé, versions d'outils, snapshots, scénario, résultats individuels, logs expurgés, autorité de signature et historique immuable de rapports. Une **signature** prouve la provenance/l'intégrité du rapport, pas automatiquement la sécurité des systèmes testés. Conserver une **matrice interne** indiquant pris en charge, échec ou non testé ; Q152 C n'exige pas de publication publique.

## Performance, budgets et veto (Q153 C)

`PerformanceBudgetPolicy` par catégorie d'application : métriques/échantillons, environnement de référence, budgets min/max, gravité et seuil de blocage. En cas de régression, expliquer la comparaison et ouvrir un **blocage** quand la criticité ou le seuil l'exige. `PerformanceException` requiert demandeur, approbation autorisée, justification, portée/version, durée/révision et audit. **Ne jamais déroger** aux critères sécurité `.htaccess`, séparation tenant, TLS, listeners, conformité ou **récupération** Q132. Les seuils exacts sont encore à définir.

## Diagnostic DNS IP publiées seulement (Q154 C)

Lire les **enregistrements A et/ou AAAA effectivement publiés** pour le domaine. Vérifier **chacune des familles présentes** : adresse destination, routage IP/public, vhost/proxy, port 80 et réponse `/.well-known/acme-challenge/`, puis certificat/HTTPS 443 après validation. Absence d'AAAA ≠ incident si seul A publié ; inversement pour IPv4. Si A et AAAA, l'une ne peut masquer la panne de l'autre. Afficher valeurs DNS à proposer et retester après intervention **manuelle** (Q143), sans écriture fournisseur.

## Redémarrage OS : politique par hôte (Q155 C)

`ServerRebootPolicy` : serveur/propriétaire, maintenance autorisée, paquet/raison, impact, approbation, hash de plan, snapshot et clé récupérables, statut du reboot, délai de health-check, reprise/compensation. Le moteur vérifie l'autorisation au moment du reboot et n'exécute jamais `shell.exec` générique. Une extension Q144 pourra gérer les groupes **plus tard** ; R4 est un hôte, et tout reboot doit préserver la réparation CLI/accès admin lorsque possible.

## Backup : déchiffrement et preuve de restauration (Q156 C)

État cible `CREATED → INTEGRITY_VERIFIED → KEY_ACCESS_VERIFIED → ISOLATED_RESTORE_PASSED → RECOVERABLE`. Q156 C requiert **export protégé de la clé/référence de secours**, **contrôle périodique d'accessibilité**, puis **vraie restauration isolée**, avec vérification fichiers/config, permissions, intégrité et PostgreSQL interne selon dépendances. Journaux d'audit sans secrets. Copier la clé sur le même disque que l'archive n'offre pas une reprise après panne physique ; KMS externe/multi-gardiens Q145 D **facultatifs**.

## Clés publiques et SFTP (Q157 C)

Le gestionnaire de site Q136 peut **enregistrer/révoquer des clés publiques SFTP** dans les limites de son compte : preuve du site/identité, politique de clé, durée, étapes sensibles approuvées, quota, racine canonique du site, sans shell par défaut, audit d'autorisation et des connexions. Les clés **privées** restent chez le client. En cas de révocation, fermer/expirer les sessions selon politique et refuser nouvelles sessions ; ne pas effacer les fichiers.

## Bêta : santé locale et consentements (Q158 C)

`BetaCohortPolicy` combine comptes-rendus manuels, checks santé **locaux** et diagnostics minimisés explicitement consentis. Consentements **distincts** selon finalité (version, diagnostic, marketing) Q6, pas de transmission automatique de contenus client. Définir seuils par **cohorte** pour bloquer nouvelles vagues et publier procédures de récupération, même lorsque les testeurs **refusent toute télémétrie** ; le Core reste utilisable hors Hub.

## Contrats éditeur différés (Q159 C, Q160 C)

Le Core pourra vérifier une **preuve signée d'installation** à la demande d'un module premium, mais **l'analyse de risque/transfert** appartient au Hub : perte d'ancienne installation, fréquence/transferts inhabituels, divergence d'organisation ou suspicion de compromission, avec second approbateur selon Q138. **Les avis** futurs ont deux vues d'un **même contenu signé/versionné** : FR/EN lisibles sur site/Panel et données structurées lisibles machine, notification paramétrable et redaction des éléments sensibles. Ne pas imposer connexion Hub au Core gratuit ni formats interop avancés non choisis.

**État : contrat candidat et matrice de tests à construire, aucune VM, backup, SFTP ou API ne fonctionne sur cette base documentaire.**
