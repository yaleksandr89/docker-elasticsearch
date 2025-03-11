# Global Elasticsearch Stack

Проект предоставляет готовый стек `Elasticsearch + analysis-icu + Kibana` с обратным прокси `Nginx` для удобного доступа.

## 📋 Предварительные требования

- Установленный Docker и Docker Compose
- 4+ GB свободной оперативной памяти
- Порт 8080 свободен на хосте

## 🗂 Структура проекта

```
.
├── docker-compose.yml
├── .env
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
    ├── elasticsearch
    └── kibana
```

## ⚙️ Конфигурация

| Переменная       | По умолчанию         | Описание                     |
| ---------------- | -------------------- | ---------------------------- |
| ELASTIC_VERSION  | 6.8.0                | Версия Elasticsearch         |
| KIBANA_VERSION   | 6.8.0                | Версия Kibana                |
| NGINX_PORT       | 8080                 | Порт для доступа через Nginx |
| ELASTIC_DATA_DIR | ./data/elasticsearch | Хранилище данных Elastic     |

## 🛠 Технические детали

- Elasticsearch конфигурация:
    - Single-node кластер
    - Выделено 1GB RAM
    - Плагин analysis-icu предустановлен
- Kibana:
    - Автоматическое ожидание готовности Elasticsearch
    - Настроен прокси через Nginx

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/global-elasticsearch.git
cd global-elasticsearch
```

### 2. Настройка окружения

```bash
cp .env.example .env
```

Отредактируйте .env при необходимости:

```ini
# Основные настройки
NGINX_PORT=8080
ELASTIC_DATA_DIR=./data/elasticsearch
KIBANA_DATA_DIR=./data/kibana
```

### 3. Запуск сервисов

```bash
docker-compose up -d --build
```

## ⚠️ Решение возможных проблем

### Ошибка загрузки образов

Если возникает ошибка авторизации при сборке (_подставить нужные версии самостоятельно_):

```bash
# Скачайте образы вручную
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.0
docker pull docker.elastic.co/kibana/kibana:6.8.0

# Повторите сборку
docker-compose build
```

## 🔌 Доступ к сервисам

Через Nginx прокси:

* Kibana: http://kibana.local:8080
* Elasticsearch: http://elastic.local:8080

**Не забудьте прописать домены**:

* Для Windows: `C:\Windows\System32\drivers\etc\hosts`
* Для Linux: `/etc/hosts`

Пример: 

```
127.0.0.1    elastic.local
127.0.0.1    kibana.local
```