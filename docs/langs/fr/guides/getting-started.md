# Premiers pas

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/getting-started.md) | [English](../../en/guides/getting-started.md) | [Español](../../es/guides/getting-started.md) | [中文](../../zh/guides/getting-started.md) | **Sélectionné** | [Deutsch](../../de/guides/getting-started.md) |

Un laboratoire local pour apprendre Elasticsearch : index, documents, recherche plein texte, filtres, agrégations et analyse de texte. Kibana offre Dev Tools et l’exploration des données ; Nginx achemine les requêtes HTTP vers le service concerné. Aucune base de produits n’est préchargée : créez l’index d’exercice en suivant le guide.

Utilisez uniquement des données synthétiques. Les processus locaux, le navigateur et les utilisateurs de Docker peuvent accéder au labo par HTTP sans authentification. Ne le publiez pas sur Internet.

## Prérequis

Git, GNU Make, Bash, curl, Docker Engine 28+ ou Docker Desktop avec Compose v2.14.2+. Linux, macOS ou Windows avec WSL2 est recommandé. La première construction nécessite l’accès aux registres officiels, aux dépôts du système et au serveur de plugins, de l’espace disque et au moins 4 Gio de mémoire disponible (6–8 Gio recommandés) ; Elasticsearch utilise un heap JVM de 2 Gio et Kibana et Docker demandent de la mémoire supplémentaire.

## Préparer l’hôte

Vérifiez les versions et les ressources avant le démarrage. Sous Linux et dans l’environnement Linux utilisé par Docker/WSL, vérifiez `vm.max_map_count` ; la recommandation officielle pour Elasticsearch actuel est `1048576`. Si la valeur est inférieure et qu’Elasticsearch signale un bootstrap check, configurez le noyau qui exécute Docker selon les [instructions officielles](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/vm-max-map-count). Ne modifiez pas l’hôte à l’aveugle. Docker Desktop alloue la mémoire à sa VM.

```bash
docker version
docker compose version
make --version
# Linux / WSL
sysctl vm.max_map_count
```

## Démarrage rapide

```bash
git clone https://github.com/yaleksandr89/docker-elasticsearch.git
cd docker-elasticsearch
make init
make config
```

Avant la construction, vérifiez le port libre, la mémoire Docker et la disponibilité des noms du projet et des trois conteneurs. Dans `make config`, vérifiez que seul le réseau `backend` existe et que seul `127.0.0.1:8080` est publié. Une seconde copie exige des noms, un port et deux répertoires distincts. Chaque utilisateur d’image doit pouvoir écrire dans son répertoire.

```bash
docker compose ls -a
docker ps -a
ls -ld data/elasticsearch data/kibana
make build
```

`make init` conserve le fichier `.docker.env` existant et crée les répertoires manquants. Il laisse les droits en place. Elasticsearch utilise l’UID 1000 et le GID principal 0. Kibana utilise l’UID 1000, le GID principal 1000 et le groupe supplémentaire 0. Ces commandes concernent une copie neuve sous Linux local avec les valeurs par défaut. Vérifiez les chemins avec `make config`, les identifiants effectifs, le propriétaire et l’absence de contenu.

```bash
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-elasticsearch
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-kibana
id
ls -ldn data/elasticsearch data/kibana
find data/elasticsearch data/kibana -mindepth 1 -maxdepth 1 -print
```

Si l’UID de l’image diffère de celui du propriétaire et manque de droits, le propriétaire peut donner accès à ces deux seuls répertoires neufs et vides. Exécutez l’exemple après confirmation de l’UID 1000 et des chemins exacts. Il nécessite les outils facultatifs `setfacl` et `getfacl` et un système de fichiers local avec ACL POSIX. Sinon, convenez d’un nouvel emplacement accessible en écriture avec le propriétaire. Préservez les répertoires existants.

```bash
setfacl -m u:1000:rwx -- data/elasticsearch data/kibana
getfacl -- data/elasticsearch data/kibana
```

```bash
make up
```

Compose démarre Kibana en arrière-plan après le contrôle HTTP d’Elasticsearch. Vérifiez sa disponibilité via /api/status. Adaptez les URL si vous changez le domaine ou le port. [Kibana](http://kibana.local:8080) · [Elasticsearch](http://elastic.local:8080)

## Connexion et disponibilité

Pour le navigateur, ajoutez ces deux entrées au fichier hosts du système où il s’exécute : Linux/macOS `/etc/hosts`, Windows `C:\Windows\System32\drivers\etc\hosts` (droits appropriés requis). Curl n’a pas besoin de modifier hosts : `--resolve` dirige la requête vers loopback avec le bon Host.

```text
127.0.0.1    elastic.local
127.0.0.1    kibana.local
```

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

La réponse racine Elasticsearch contient `version.number` et `cluster_name` ; `_cluster/health` indique l’état. `green` signifie que tous les shards sont disponibles, `yellow` sur un nœud peut signaler des réplicas non assignés et `red` exige un diagnostic. Les deux plugins doivent apparaître dans `_cat/plugins`. Kibana est prête lorsque `/api/status` indique `status.overall.level: available` ; des 502/503 sont possibles avant. Ouvrez ensuite [Kibana](http://kibana.local:8080) et Dev Tools → Console.

[Diagnostic du démarrage](troubleshooting.md) · [Exercices de recherche et d’analyse de texte](search-lab.md)

## Captures historiques

Les illustrations d’origine de l’ancien laboratoire (Elasticsearch 6.8.0) sont conservées. Les versions actuelles diffèrent en présentation, menus et réponses ; ces images ne valident pas un lancement actuel.

![Elasticsearch 6.8.0 — réponse racine](../../../assets/elastic-local-1.png)

![Elasticsearch 6.8.0 — réponse de recherche](../../../assets/elastic-local-2.png)

![Kibana — aperçu du cluster](../../../assets/kibana-local-1.png)

![Kibana — documents dans Discover](../../../assets/kibana-local-2.png)

![Kibana — console Dev Tools](../../../assets/kibana-local-3.png)

## Documentation

- [Exercices de recherche et d’analyse de texte](search-lab.md)
- [Exploitation et commandes Make](operations.md)
- [Diagnostic](troubleshooting.md)
- [Architecture et configuration](../reference/configuration.md)
- [Contribuer](../CONTRIBUTING.md)
