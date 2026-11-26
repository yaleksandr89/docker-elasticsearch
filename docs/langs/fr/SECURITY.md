# Politique de sécurité

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/SECURITY.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/SECURITY.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/SECURITY.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/SECURITY.md) | **Français** | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/SECURITY.md) |

## Versions prises en charge

Les correctifs de sécurité sont envisagés pour l’état actuel de `master` et la dernière version publiée. Les anciennes versions peuvent avoir une configuration réseau différente ; vérifiez la compatibilité des données avant toute mise à niveau.

| Version | Prise en charge |
|---|---|
| `master` | Oui |
| Dernière version publiée | Oui |

## Périmètre de sécurité du laboratoire

Ce laboratoire local d’apprentissage utilise des données synthétiques ; ce n’est pas un déploiement de production. Dans la configuration actuelle, Elasticsearch fonctionne sans authentification ni TLS ; par défaut, seul Nginx est publié sur `127.0.0.1`, et les ports internes d’Elasticsearch et de Kibana ne sont pas publiés sur l’hôte. Avec `WITH_EXTERNAL_NETWORK=1`, les membres du réseau Docker de confiance sélectionné accèdent à Elasticsearch sans authentification. Ce comportement est intentionnel et ne constitue pas en soi une vulnérabilité. Ne connectez pas de réseaux non fiables et n’utilisez pas de données réelles.

Les problèmes de sécurité comprennent notamment :

- publication imprévue de services hors loopback ou connexion à un réseau externe sans activation explicite ;
- contournement des restrictions de routage Nginx attendues ou exposition de fichiers internes ou de configuration ;
- traitement non sûr de paramètres ou chemins entraînant l’exécution de commandes ou la modification de données d’autrui ;
- suppression, écrasement ou divulgation imprévus de données pendant les opérations du laboratoire ;
- problèmes d’images, de plugins ou de CI affectant la sécurité du projet.

Signalez les bugs ordinaires via [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues), les questions et idées via [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions). Si le problème concerne un composant amont, précisez sa version exacte et son impact sur le laboratoire ; signalez également les défauts du composant à ses mainteneurs selon leurs règles.

## Signaler une vulnérabilité

Privilégiez GitHub Private Vulnerability Reporting : ouvrez **Security and quality → Report a vulnerability**. Si cette option est indisponible, demandez un canal privé dans GitHub Discussions sans publier de détails techniques de la vulnérabilité.

Ne publiez pas de mots de passe, jetons, configurations locales ou de production, données réelles, logs complets, exploits fonctionnels ou détails sensibles avant la divulgation coordonnée. Utilisez uniquement des données synthétiques ou des extraits nettoyés.

## Contenu du rapport

- Release, branch ou commit concerné et versions d’Elasticsearch, Kibana, Nginx, Docker et Compose si pertinentes.
- Mode de lancement (local ou intégration), limite d’accès attendue et impact potentiel.
- Étapes minimales de reproduction, comportement attendu et réel.
- Extraits nettoyés de requêtes, réponses ou logs et correctif possible s’il est connu.

## Traitement du rapport

Les rapports sont examinés selon les disponibilités ; aucun SLA fixe n’est promis. Coordonnez la divulgation avec le mainteneur. Après confirmation, les correctifs et les informations sur les versions affectées sont publiés dans le cadre d’une divulgation coordonnée. Aucun programme de récompense des vulnérabilités n’est annoncé.
