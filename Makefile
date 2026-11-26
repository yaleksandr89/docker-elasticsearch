SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := init

# Trusted local Make-compatible assignments, also used by Compose.
-include .docker.env
settings := COMPOSE_PROJECT_NAME ELASTIC_VERSION KIBANA_VERSION NGINX_VERSION ELASTIC_CONTAINER KIBANA_CONTAINER NGINX_CONTAINER ELASTIC_DOMAIN KIBANA_DOMAIN ELASTIC_PORT KIBANA_PORT NGINX_PORT ELASTIC_DATA_DIR KIBANA_DATA_DIR EXTERNAL_NETWORK
export $(settings)

COMPOSE_COMMAND ?= docker compose
WITH_EXTERNAL_NETWORK ?= 0
files := -f docker-compose.yml
ifeq ($(WITH_EXTERNAL_NETWORK),1)
files += -f docker-compose.external.yml
else ifneq ($(WITH_EXTERNAL_NETWORK),0)
$(error WITH_EXTERNAL_NETWORK must be 0 or 1)
endif
compose = $(COMPOSE_COMMAND) --env-file .docker.env $(files)

.PHONY: help identity init directories validate pull build config up down reset restart in log
help:
	@printf '%s\n' \
	    'make help           Show this help / Показать справку' \
	    'make init           Create missing settings and data directories / Создать недостающий файл настроек и каталоги данных' \
	    'make pull           Pull pinned base images / Скачать базовые образы указанных версий' \
	    'make build          Build images without cache / Собрать образы без кеша' \
	    'make config         Show resolved Compose configuration / Показать итоговую конфигурацию Compose' \
	    'make up             Start in the background; check Kibana readiness separately / Запустить в фоне; готовность Kibana проверить отдельно' \
	    'make down           Stop and remove containers, keeping data / Остановить и удалить контейнеры, сохранив данные' \
	    'make reset          Run down then up to recreate containers without deleting indices / Выполнить down, затем up без удаления индексов' \
	    'make restart        Restart without applying configuration changes / Перезапустить без применения изменений конфигурации' \
	    'make in SERVICE     Open Bash, e.g. make in elasticsearch / Открыть Bash, например make in elasticsearch' \
	    'make log SERVICE    Show logs, e.g. make log kibana / Показать журналы, например make log kibana' \
	    'SERVICE             elasticsearch, kibana, nginx / Допустимые имена: elasticsearch, kibana, nginx' \
	    'WITH_EXTERNAL_NETWORK=0|1  Local by default (0); opt in (1) / По умолчанию локальный режим (0); подключение по запросу (1)' \
	    'EXTERNAL_NETWORK    Existing trusted network; peers can access Elasticsearch without authentication / Существующая доверенная сеть; её участники получают доступ к Elasticsearch без аутентификации' \
	    'make config WITH_EXTERNAL_NETWORK=1  Inspect integration settings / Проверить настройки подключения' \
	    'make up WITH_EXTERNAL_NETWORK=1      Start with integration / Запустить с подключением к внешней сети' \
	    'make down WITH_EXTERNAL_NETWORK=1    Stop, keeping data and the external network / Остановить, сохранив данные и внешнюю сеть'

init:
	@if [[ ! -e .docker.env ]]; then (set -C; cat .docker.env.example > .docker.env); fi
	@$(MAKE) --no-print-directory directories

directories: validate
	@mkdir -p -- "$$ELASTIC_DATA_DIR" "$$KIBANA_DATA_DIR"

validate:
	@test -f .docker.env || { echo 'Run make init first.' >&2; exit 1; }
	@$(compose) config --quiet
	@bash docker-configs/nginx/start-nginx.sh
	@[[ $$ELASTIC_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$$ && $$KIBANA_VERSION == "$$ELASTIC_VERSION" && $$NGINX_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$$ ]] || { echo 'Use exact image tags and matching Elasticsearch/Kibana versions.' >&2; exit 1; }
	@[[ $$NGINX_PORT =~ ^[1-9][0-9]{0,4}$$ && $$NGINX_PORT -le 65535 ]] || { echo 'Invalid NGINX_PORT.' >&2; exit 1; }
	@[[ -n $$COMPOSE_PROJECT_NAME && $$ELASTIC_CONTAINER != "$$KIBANA_CONTAINER" && $$ELASTIC_CONTAINER != "$$NGINX_CONTAINER" && $$KIBANA_CONTAINER != "$$NGINX_CONTAINER" ]] || { echo 'Set a project name and distinct container names.' >&2; exit 1; }

# Compose project names are daemon-wide. Check ownership even for stopped services.
identity:
	@[[ $$COMPOSE_PROJECT_NAME =~ ^[a-z0-9][a-z0-9_-]*$$ ]] || { echo 'Invalid COMPOSE_PROJECT_NAME.' >&2; exit 1; }
	@set -e; ids=$$(docker ps -aq --filter "label=com.docker.compose.project=$$COMPOSE_PROJECT_NAME"); \
	for id in $$ids; do \
	    directory=$$(docker inspect --format '{{index .Config.Labels "com.docker.compose.project.working_dir"}}' "$$id"); \
	    [[ "$$directory" == "$$(pwd -P)" ]] || { echo 'Project belongs to another checkout.' >&2; exit 1; }; \
	done

pull: validate
	docker pull "docker.elastic.co/elasticsearch/elasticsearch:$$ELASTIC_VERSION"
	docker pull "docker.elastic.co/kibana/kibana:$$KIBANA_VERSION"
	docker pull "nginx:$$NGINX_VERSION"

build: validate identity
	$(compose) build --no-cache

config: validate
	$(compose) config

up: validate identity
	$(compose) up -d

down: identity
	$(compose) down

reset: validate identity
	$(compose) down
	$(compose) up -d

restart: validate identity
	$(compose) restart

ifneq ($(filter in log,$(firstword $(MAKECMDGOALS))),)
service := $(word 2,$(MAKECMDGOALS))
ifneq ($(words $(MAKECMDGOALS)),2)
$(error Use make in SERVICE or make log SERVICE)
endif
ifeq ($(filter elasticsearch kibana nginx,$(service)),)
$(error Unknown service)
endif
.PHONY: $(service)
$(service):
	@:
endif

in: identity
	$(compose) exec $(service) bash

log: identity
	$(compose) logs $(service)
