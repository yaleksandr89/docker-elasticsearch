# Global Elasticsearch Stack

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Choisissez la Langue :

| Русский  | English                              | Español                              | 中文                              | Français                              | Deutsch                              |
|-----------|--------------------------------------|--------------------------------------|-------------------------------------|--------------------------------------|--------------------------------------|
| [Русский](../README.md) | [English](./README_en.md) | [Español](./README_es.md) | [中文](./README_zh.md) | **Sélectionné** | [Deutsch](./README_de.md) |

Le projet fournit une stack prête à l'emploi avec `Elasticsearch + analysis-icu + analysis-phonetic + Kibana` et un proxy inversé `Nginx` pour un accès pratique.

## 📋 Prérequis

- Docker 20.10+ et Docker Compose 2.0+
- 4+ Go de RAM libre
- Les ports 8080 et 9200 doivent être libres sur l'hôte
- Réseau Docker existant `external_network` (**si ce n'est pas nécessaire, supprimez-le du docker-compose.yml**)

## 🗂 Structure du projet

```
.
├── .docker.env (créé par la commande ou manuellement)
├── .docker.env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── README.md
├── langs
│   ├── ...fichiers de localisation README.md...
├── assets
│   ├── ...contenu pour README.md...
├── docker-configs
│   ├── elasticsearch
│   │   ├── Dockerfile
│   │   └── elasticsearch.yml
│   ├── kibana
│   │   ├── Dockerfile
│   │   ├── kibana.yml
│   │   └── wait-for-elastic.sh
│   └── nginx
│       ├── Dockerfile
│       └── default.conf.template
└── data
├── ...créé pour le projet dans .env...
```

## ⚙️ Configuration

Les principales variables d'environnement (fichier `.docker.env`):

| Variable             | Valeur par défaut    | Description                            |
|----------------------|----------------------|----------------------------------------|
| COMPOSE_PROJECT_NAME | elasticsearch        | Nom du projet                          |
| ELASTIC_VERSION      | latest               | Version d'Elasticsearch                |
| KIBANA_VERSION       | latest               | Version de Kibana                      |
| NGINX_VERSION        | latest               | Version de Nginx                       |
| ELASTIC_CONTAINER    | elasticsearch        | Nom du conteneur Elasticsearch         |
| KIBANA_CONTAINER     | kibana               | Nom du conteneur Kibana                |
| NGINX_CONTAINER      | nginx                | Nom du conteneur Nginx                 |
| KIBANA_DOMAIN        | kibana.local         | Domaine pour accéder à Kibana          |
| ELASTIC_DOMAIN       | elastic.local        | Domaine pour accéder à Elasticsearch   |
| KIBANA_PORT          | 5601                 | Port de Kibana sur l'hôte              |
| ELASTIC_PORT         | 9200                 | Port d'Elasticsearch sur l'hôte        |
| NGINX_PORT           | 80                   | Port de Nginx sur l'hôte               |
| ELASTIC_DATA_DIR     | ./data/elasticsearch | Répertoire des données d'Elasticsearch |
| KIBANA_DATA_DIR      | ./data/kibana        | Répertoire des données de Kibana       |
| EXTERNAL_NETWORK     | external_network     | Réseau Docker externe                  |

## 🛠 Détails techniques

- **Elasticsearch**:
    - Cluster à un seul nœud
    - 2 Go de RAM alloués
    - Le plugin `analysis-icu` est préinstallé
    - Le plugin `analysis-phonetic` est préinstallé
    - Configuration des synonymes via `synonyms.txt`
- **Kibana**:
    - Attente automatique de la disponibilité d'Elasticsearch
    - Proxy configuré via Nginx
- **Nginx**:
    - Proxy inversé pour Elasticsearch et Kibana

## 🚀 Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/yourusername/docker-elasticsearch.git
cd docker-elasticsearch
```

### 2. Initialiser l'environnement

Si vous utilisez Windows, consultez le fichier `Makefile` pour une description complète des commandes. Il est recommandé d'utiliser `Linux` ou `Windows + WSL`.

#### 2.1 Initialiser `.docker.env`

Exécutez :

```makefile
make init
```

Le fichier `.docker.env` sera créé, ainsi que les répertoires où les fichiers seront stockés (spécifiés dans les variables : `ELASTIC_DATA_DIR`, `KIBANA_DATA_DIR`).

#### 2.2 Télécharger les images Elasticsearch, Kibana, Nginx

Exécutez :

```makefile
make pull
```

Les images seront téléchargées avec les versions spécifiées dans `ELASTIC_VERSION`, `KIBANA_VERSION`, `NGINX_VERSION`.

#### 2.3 Lancer le projet

Exécutez :

```makefile
make up
```

Si une erreur apparaît lors du lancement :

```text
network onex_backend declared as external, but could not be found
```

![make-up-error.png](../assets/make-up-error.png)

Cela signifie que vous n'avez pas spécifié de réseau externe (le réseau du projet auquel Elasticsearch doit se connecter). Deux options :

1. Spécifiez le réseau existant dans `.docker.env`, en configurant le paramètre `EXTERNAL_NETWORK`
2. Supprimez-le de `docker-compose.yml`
```
Dans le service Elasticsearch :
- external_network

Dans networks :
external_network:
name: ${EXTERNAL_NETWORK}
external: true
```

#### 2.4 Autres commandes

- Construire les images sans cache : `make build`
- Arrêter les conteneurs : `make down`
- Redémarrage "dur" : `make reset`
- Redémarrage "doux" : `make restart`
- Entrer dans le conteneur requis : `make in <container>`
- Voir les journaux du conteneur requis : `make log <container>`

## 🔌 Accès aux services

Une fois le projet démarré, les services seront accessibles via Nginx :

- Kibana : http://`${KIBANA_DOMAIN}`:`${NGINX_PORT}`
- Elasticsearch : http://`${ELASTIC_DOMAIN}`:`${NGINX_PORT}`

Par défaut :

- Kibana : http://kibana.local:80
- Elasticsearch : http://elastic.local:80

**N'oubliez pas d'ajouter les domaines dans votre fichier hosts** :

* Sous Windows : `C:\Windows\System32\drivers\etc\hosts`
* Sous Linux : `/etc/hosts`

Exemple :

```
127.0.0.1    elastic.local
127.0.0.1    kibana.local
```

# Résultat

Accès à Elasticsearch via le navigateur (http://elastic.local:80) :

![elastic-local-1.png](../assets/elastic-local-1.png)

![elastic-local-2.png](../assets/elastic-local-2.png)

Accès à Kibana via le navigateur (http://kibana.local:80) :

![kibana-local-1.png](../assets/kibana-local-1.png)

![kibana-local-2.png](../assets/kibana-local-2.png)

![kibana-local-3.png](../assets/kibana-local-3.png)