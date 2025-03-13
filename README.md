# Global Elasticsearch Stack

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Выберите язык:

| Русский    | English                              | Español                              | 中文                              | Français                              | Deutsch                              |
|------------|--------------------------------------|--------------------------------------|---------------------------------|---------------------------------------|--------------------------------------|
| **Выбран** | [English](./langs/README_en.md) | [Español](./langs/README_es.md) | [中文](./langs/README_zh.md) | [Français](./langs/README_fr.md) | [Deutsch](./langs/README_de.md) |

Проект предоставляет готовый стек `Elasticsearch + analysis-icu + analysis-phonetic + Kibana` с обратным прокси `Nginx` для удобного доступа.

## 📋 Предварительные требования

- Docker 20.10+ и Docker Compose 2.0+
- 4+ GB свободной оперативной памяти
- Порты 8080 и 9200 свободны на хосте
- Существующая Docker сеть `external_network` (**если не требуется нужно удалить из docker-compose.yml**)

## 🗂 Структура проекта

```
.
├── .docker.env (создается командой или вручную)
├── .docker.env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── README.md
├── langs
│   ├── ...файлы локализации README.md...
├── assets
│   ├── ...контент для README.md...
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
    ├── ...создается под проект в .env...
```

## ⚙️ Конфигурация

Основные переменные окружения (файл `.docker.env`):

| Переменная           | По умолчанию         | Описание                          |
|----------------------|----------------------|-----------------------------------|
| COMPOSE_PROJECT_NAME | elasticsearch        | Название проекта                  |
| ELASTIC_VERSION      | latest               | Версия Elasticsearch              |
| KIBANA_VERSION       | latest               | Версия Kibana                     |
| NGINX_VERSION        | latest               | Версия Nginx                      |
| ELASTIC_CONTAINER    | elasticsearch        | Название контейнера elasticsearch |
| KIBANA_CONTAINER     | kibana               | Название контейнера kibana        |
| NGINX_CONTAINER      | nginx                | Название контейнера nginx         |
| KIBANA_DOMAIN        | kibana.local         | Домен для доступа к Kibana        |
| ELASTIC_DOMAIN       | elastic.local        | Домен для доступа к Elasticsearch |
| KIBANA_PORT          | 5601                 | Порт kibana на хосте              |
| ELASTIC_PORT         | 9200                 | Порт elasticsearch на хосте       |
| NGINX_PORT           | 80                   | Порт Nginx на хосте               |
| ELASTIC_DATA_DIR     | ./data/elasticsearch | Хранилище данных Elasticsearch    |
| KIBANA_DATA_DIR      | ./data/kibana        | Хранилище данных Kibana           |
| EXTERNAL_NETWORK     | external_network     | Внешняя сеть Docker               |

## 🛠 Технические детали

- **Elasticsearch**:
  - Single-node кластер
  - Выделено 2GB RAM
  - Плагин `analysis-icu` предустановлен
  - Плагин `analysis-phonetic` предустановлен
  - Конфигурация с синонимами через `synonyms.txt`
- **Kibana**:
  - Автоматическое ожидание готовности Elasticsearch
  - Настроен прокси через Nginx
- **Nginx**:
  - Обратный прокси для Elasticsearch и Kibana

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/docker-elasticsearch.git
cd docker-elasticsearch
```

### 2. Инициализация окружения

Если вы используете Windows - смотрите файл `Makefile` - там есть полное описание команд. Рекомендую использовать или `Linux` или `Windows + WSL`.

#### 2.1 инициализация .docker.env

Выполнить:

```makefile
make init
```

В директории будет создан файл `.docker.env`, а также директории в которых будут храниться файлы (указываются в переменных: `ELASTIC_DATA_DIR`, `KIBANA_DATA_DIR`)

#### 2.2 Скачать образы elasticsearch, kibana, nginx

Выполнить:

```makefile
make pull
```

Будут скачены образы с версией указанной в `ELASTIC_VERSION`, `KIBANA_VERSION`, `NGINX_VERSION`.

#### 2.2 Запустить проект

Выполнить:

```makefile
make up
```

Если в процессе запуска возникла ошибка:

```text
network onex_backend declared as external, but could not be found
```

![make-up-error.png](./assets/make-up-error.png)

Это означает, что вы не указали внешнюю сеть (сеть проекта, к которой нужно подключить elasticsearch). Варианта 2:

1. Указать в существующую сеть в `.docker.env`, параметр `EXTERNAL_NETWORK`
2. Удалить из `docker-compose.yml`
```
У сервиса elasticsearch:
- external_network

У networks:
external_network:
  name: ${EXTERNAL_NETWORK}
  external: true
```

#### 2.3 Остальные команды

- Сборка образов без кэша: `make build`
- Останавливает контейнеры: `make down`
- "Жесткий" перезапуск: `make reset`
- "Мягкий" перезапуск: `make restart`
- Войти в нужный контейнер: `make in <container>`
- Просмотреть логи нужного контейнера: `make log <container>`

## 🔌 Доступ к сервисам

После запуска доступны через Nginx:

- Kibana: http://`${KIBANA_DOMAIN}`:`${NGINX_PORT}`
- Elasticsearch: http://`${ELASTIC_DOMAIN}`:`${NGINX_PORT}`

По умолчанию:

- Kibana: http://kibana.local:80
- Elasticsearch: http://elastic.local:80

**Не забудьте прописать домены**:

* Для Windows: `C:\Windows\System32\drivers\etc\hosts`
* Для Linux: `/etc/hosts`

Пример: 

```
127.0.0.1    elastic.local
127.0.0.1    kibana.local
```

# Результат

Доступ к Elasticsearch через браузер (http://elastic.local:80):

![elastic-local-1.png](./assets/elastic-local-1.png)

![elastic-local-2.png](./assets/elastic-local-2.png)

Доступ к Kibana через браузер (http://kibana.local:80):

![kibana-local-1.png](./assets/kibana-local-1.png)

![kibana-local-2.png](./assets/kibana-local-2.png)

![kibana-local-3.png](./assets/kibana-local-3.png)