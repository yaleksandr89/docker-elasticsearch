# Эксплуатация и Make-команды

## Выберите язык

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| **Выбран** | [English](../../en/guides/operations.md) | [Español](../../es/guides/operations.md) | [中文](../../zh/guides/operations.md) | [Français](../../fr/guides/operations.md) | [Deutsch](../../de/guides/operations.md) |

По умолчанию стенд работает в локальном режиме. Перед запуском подготовьте каталоги данных по инструкции ниже.

[Начало работы](getting-started.md)

## Быстрый старт

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| Команда | Действие |
|---|---|
| `make help` | Показывает двуязычную справку. |
| `make init` | Создаёт `.docker.env` при отсутствии и каталоги из двух переменных `*_DATA_DIR`; не изменяет существующую конфигурацию. |
| `make pull` | Скачивает базовые образы из официальных registry по версиям из Make-конфигурации; не пересобирает локальные образы. |
| `make build` | Собирает образы без кэша. |
| `make config` | Показывает итоговую Compose-конфигурацию без запуска. |
| `make up` | После успешной HTTP-проверки Elasticsearch Compose запускает Kibana в фоне. Проверьте готовность Kibana через /api/status. При смене домена или порта измените адреса в примерах. |
| `make down` | Останавливает и удаляет контейнеры и управляемую сеть, но не каталог данных на хосте. |
| `make reset` | Последовательно выполняет `down` и `up -d`, пересоздаёт контейнеры и сохраняет данные и индексы. |
| `make restart` | Перезапускает имеющиеся контейнеры; изменения образов, Compose и переменных не применяет. |
| `make in elasticsearch` | Запускает Bash в выбранном сервисе. Допустимые имена: `elasticsearch`, `kibana`, `nginx`. |
| `make log kibana` | Выводит логи выбранного сервиса; не следует за потоком автоматически. |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## Подключение отдельного проекта

Узнайте фактическое имя существующей доверенной сети приложения через `docker network ls`, сверив участников через `docker network inspect`. Укажите её в `EXTERNAL_NETWORK` файла `.docker.env`. Compose объединит базовый файл и расширение, оставит `backend` и подключит к дополнительной сети только Elasticsearch. Из контейнера приложения используйте `http://docker-elasticsearch-es:9200` или фактическое имя `ELASTIC_CONTAINER`. Все участники сети получают доступ без аутентификации. Используйте тот же флаг для последующих команд, в том числе остановки.

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

Перед сменой режима выполните `down` с прежним набором файлов или флагом, сохраните оба пути данных и выполните `up` с новым набором. Внешняя сеть остаётся у её владельца. Не используйте чужие сети и каталоги. `restart` сохраняет сетевые настройки существующих контейнеров.

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## Хранение данных и обновления

Оба bind mount переживают пересоздание. Большая часть сохранённых объектов Kibana находится в системных индексах Elasticsearch. Перед остановкой прежнего стенда проверьте `/usr/share/kibana/data` в его контейнере и отдельно сохраните нужные локальные файлы.

В Make нет целей автоматической очистки, создания снимков или восстановления. Копия каталога работающего Elasticsearch не заменяет резервную копию. До остановки запишите реальные версии, имена контейнеров, порт и оба пути монтирования. При необходимости сделайте официальный [снимок](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore), проверьте восстановление в отдельном стенде и совместимость плагинов для каждого этапа [поддерживаемого обновления](https://www.elastic.co/docs/deploy-manage/upgrade). Для прежних клиентов сохраните заданное имя `ELASTIC_CONTAINER` (например, `global-elasticsearch`). Меняйте прежний порт 80 на 8080 только намеренно. Обновление выполняется отдельно по решению владельца.

Остановите прежний стенд с его конфигурацией. Для неизвестной исходной версии сначала выясните совместимость. Понижение версии на уже обновлённых данных небезопасно.

## Проверки

CI запускается для push и pull request в `master`, а также вручную через Actions. `quality` проверяет синтаксис startup-скриптов, учебные fixtures и resolved Compose; `docker-smoke` собирает отдельный стенд на фиксированных версиях, проверяет HTTP через оба virtual host, плагины и учебный поиск. Факт успешного запуска подтверждают результаты CI, а не наличие workflow.

Python 3 нужен только для проверок fixtures и CI.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Запускайте `tests/smoke.py` только в одноразовой копии. Локально он проверяет путь `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate` и имя проекта `elastic-learning-test-xxxxxxxx`, где суффикс — те же восемь букв или цифр в нижнем регистре. Перед созданием индекса скрипт сверяет метки, образы, сеть, публикацию и оба каталога. Режим `--persisted` проверяет ранее созданные документы.

## Документация

- [Начало работы](getting-started.md)
- [Практика поиска и анализа текста](search-lab.md)
- [Диагностика](troubleshooting.md)
- [Архитектура и конфигурация](../reference/configuration.md)
- [Участие в разработке](../../../../.github/CONTRIBUTING.md)
