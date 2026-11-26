# Exploitation et commandes Make

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/operations.md) | [English](../../en/guides/operations.md) | [Español](../../es/guides/operations.md) | [中文](../../zh/guides/operations.md) | **Sélectionné** | [Deutsch](../../de/guides/operations.md) |

Le labo utilise le mode local par défaut. Préparez les répertoires suivant le guide de démarrage avant de lancer les services.

[Premiers pas](getting-started.md)

## Démarrage rapide

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| Commande | Effet |
|---|---|
| `make help` | Affiche l’aide bilingue. |
| `make init` | Crée `.docker.env` si absent et les répertoires `*_DATA_DIR` ; conserve la configuration existante. |
| `make pull` | Télécharge les images de base officielles selon les versions Make ; ne reconstruit pas les images locales. |
| `make build` | Construit sans cache. |
| `make config` | Affiche la configuration Compose résolue sans lancer les services. |
| `make up` | Compose démarre Kibana en arrière-plan après le contrôle HTTP d’Elasticsearch. Vérifiez sa disponibilité via /api/status. Adaptez les URL si vous changez le domaine ou le port. |
| `make down` | Arrête et supprime conteneurs et réseau géré, pas le répertoire de données hôte. |
| `make reset` | Exécute `down` puis `up -d`, recrée les conteneurs et conserve les données et les index. |
| `make restart` | Redémarre les conteneurs existants sans appliquer les changements d’image, Compose ou variables. |
| `make in elasticsearch` | Lance Bash dans le service choisi : `elasticsearch`, `kibana`, `nginx`. |
| `make log kibana` | Affiche les logs du service sans suivi automatique. |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## Connecter un autre projet

Repérez le réseau existant et de confiance de l’application avec `docker network ls` et vérifiez ses membres avec `docker network inspect`. Renseignez son nom réel dans `EXTERNAL_NETWORK` dans `.docker.env`. Compose fusionne les fichiers, conserve `backend` et ajoute seulement Elasticsearch au réseau supplémentaire. Depuis le conteneur applicatif, utilisez `http://docker-elasticsearch-es:9200` ou le nom réel de `ELASTIC_CONTAINER`. Tous les membres accèdent sans authentification. Gardez ce paramètre pour les commandes suivantes, y compris l’arrêt.

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

Pour changer de mode, lancez `down` avec les anciens fichiers ou l’ancienne option, gardez les deux chemins de données, puis lancez `up` avec le nouveau réglage. Le réseau externe reste à son propriétaire. Utilisez uniquement le réseau et les chemins convenus. `restart` garde les réglages réseau des conteneurs existants.

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## Persistance et mises à jour

Les deux montages persistent après recréation. Kibana stocke la plupart des objets dans les index système d’Elasticsearch. Avant d’arrêter l’ancien labo, inspectez `/usr/share/kibana/data` dans son conteneur et gardez à part les fichiers locaux nécessaires.

Make ne possède aucune cible de nettoyage, de snapshot ou de restauration automatique. Copier le répertoire d’un Elasticsearch actif donne une sauvegarde peu fiable. Avant l’arrêt, relevez versions, noms des conteneurs, port et chemins des deux montages. Si nécessaire, créez un [snapshot](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore), testez la restauration dans un autre labo et vérifiez la compatibilité des extensions à chaque étape du [parcours pris en charge](https://www.elastic.co/docs/deploy-manage/upgrade). Gardez la valeur d’`ELASTIC_CONTAINER` pour les clients existants, par exemple `global-elasticsearch`. Changez l’ancien port 80 vers 8080 uniquement si prévu. Le propriétaire décide à part de la mise à niveau.

Arrêtez l’ancien labo avec sa configuration d’origine. Si la version source est inconnue, établissez d’abord la compatibilité. Une rétrogradation sur des données mises à niveau est dangereuse.

## Vérifications

CI s’exécute sur push et pull request vers `master`, ainsi que manuellement via Actions. `quality` vérifie la syntaxe des scripts, les fixtures et Compose résolu ; `docker-smoke` construit un laboratoire isolé à versions fixes et vérifie HTTP via deux hôtes virtuels, plugins et recherche. Seuls les résultats CI établissent le succès.

Python 3 est nécessaire seulement pour les vérifications des fixtures et le CI.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Exécutez `tests/smoke.py` uniquement dans une copie jetable. En local, il exige `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate` et le projet `elastic-learning-test-xxxxxxxx`, avec les mêmes huit caractères alphanumériques en minuscules dans le nom. Avant de créer l’index, il vérifie les étiquettes, images, réseau, port et deux montages. `--persisted` vérifie les documents créés précédemment.

## Documentation

- [Premiers pas](getting-started.md)
- [Exercices de recherche et d’analyse de texte](search-lab.md)
- [Diagnostic](troubleshooting.md)
- [Architecture et configuration](../reference/configuration.md)
- [Contribuer](../CONTRIBUTING.md)
