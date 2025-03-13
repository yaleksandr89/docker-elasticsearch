SHELL = bash
.PHONY: init pull up restart in log down

# Тут собираются образы для работы контейнеров

# запоминаем каталог проекта
PROJECT_DIR := $(PWD)

# переменные ENV
ENV_FILE_EXAMPLE := .docker.env.example
ENV_FILE := .docker.env

-include $(ENV_FILE)

COMPOSE_COMMAND := docker-compose -p $(COMPOSE_PROJECT_NAME) --env-file $(ENV_FILE)

# Определяем контейнеры для работы
LOCAL_CONTAINERS := elasticsearch kibana nginx

# Подготавливаем окружение (создаем .docker.env, если его нет)
init:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		cp $(ENV_FILE_EXAMPLE) $(ENV_FILE); \
		echo "Создан файл $(ENV_FILE) из примера"; \
	else \
		echo "Файл $(ENV_FILE) уже существует"; \
	fi

	@echo "Проверяем переменные и создаем директории для данных..."
	@ELASTIC_DIR=$$(grep '^ELASTIC_DATA_DIR=' $(ENV_FILE) | cut -d '=' -f2); \
	KIBANA_DIR=$$(grep '^KIBANA_DATA_DIR=' $(ENV_FILE) | cut -d '=' -f2); \
	for DIR in "$$ELASTIC_DIR" "$$KIBANA_DIR"; do \
		if [ -n "$$DIR" ] && [ ! -d "$$DIR" ]; then \
			mkdir -p "$$DIR"; \
			echo "Создана директория: $$DIR"; \
		fi; \
	done

# Для получения образов (скачиваем актуальные образы Docker)
pull:
	@echo "Скачиваем Docker образы для Elasticsearch, Kibana и Nginx..."
	docker pull docker.elastic.co/elasticsearch/elasticsearch:$(ELASTIC_VERSION)
	docker pull docker.elastic.co/kibana/kibana:$(KIBANA_VERSION)
	docker pull nginx:$(NGINX_VERSION)
	@echo "Образы успешно скачаны."

# Сборка образов без кэша
build:
	@echo "Собираем Docker образы..."
	$(COMPOSE_COMMAND) build --no-cache

# Запускаем контейнеры
up:
	$(COMPOSE_COMMAND) up -d

# Останавливаем контейнеры
down:
	$(COMPOSE_COMMAND) down

# "Жесткий" перезапуск
reset: down up

# "Мягкий" перезапуск
restart:
	$(COMPOSE_COMMAND) restart

# Выполняем команду в контейнере
ifeq (in,$(firstword $(MAKECMDGOALS)))
  CONTAINER := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(CONTAINER):;@:)
endif

in:
	@test -n "$(CONTAINER)"  || (echo "Не указан контейнер. Используйте \"make in nginx\" в качестве примера" && exit 1)
	$(COMPOSE_COMMAND) exec $(CONTAINER) bash

# Просмотр логов контейнера
ifeq (log,$(firstword $(MAKECMDGOALS)))
  CONTAINER := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(CONTAINER):;@:)
endif

log:
	@test -n "$(CONTAINER)"  || (echo "Не указан контейнер. Используйте \"make log nginx\" в качестве примера" && exit 1)
	$(COMPOSE_COMMAND) logs $(CONTAINER)
