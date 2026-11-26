# Начало работы

## Выберите язык

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| **Выбран** | [English](../../en/guides/getting-started.md) | [Español](../../es/guides/getting-started.md) | [中文](../../zh/guides/getting-started.md) | [Français](../../fr/guides/getting-started.md) | [Deutsch](../../de/guides/getting-started.md) |

Локальный учебный стенд для знакомства с Elasticsearch: индексы, документы, полнотекстовый поиск, фильтры, агрегации и анализ текста. Kibana позволяет выполнять запросы в Dev Tools и исследовать данные; Nginx направляет HTTP-запросы к нужному сервису. Стенд не содержит готовой базы товаров: учебный индекс создаётся по руководству.

Только для обучения на синтетических данных. Локальные процессы, браузер и пользователи Docker могут обращаться к стенду по HTTP без пароля. Не публикуйте его в интернете.

## Требования

Git, GNU Make, Bash, curl, Docker Engine 28+ или Docker Desktop с Compose v2.14.2+. Рекомендуется Linux, macOS или Windows с WSL2. Для первоначальной сборки нужны доступ к официальным registry, репозиториям ОС и серверу плагинов, свободный диск и минимум 4 ГиБ доступной памяти (лучше 6–8 ГиБ); 2 ГиБ выделены JVM Elasticsearch, а Kibana и Docker требуют дополнительную память.

## Подготовка хоста

Проверьте версии и доступные ресурсы до запуска. На Linux и в Linux-среде Docker/WSL проверьте `vm.max_map_count`; для современной ветки Elasticsearch официальный ориентир — `1048576`. Если значение ниже и Elasticsearch сообщает о bootstrap check, настройте именно ядро, на котором работает Docker, по [официальной инструкции](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/vm-max-map-count). Не выполняйте системные изменения вслепую. На Docker Desktop память выделяется виртуальной машине.

```bash
docker version
docker compose version
make --version
# Linux / WSL
sysctl vm.max_map_count
```

## Быстрый старт

```bash
git clone https://github.com/yaleksandr89/docker-elasticsearch.git
cd docker-elasticsearch
make init
make config
```

Перед сборкой проверьте свободный порт, память Docker, уникальность проекта и трёх имён контейнеров. В выводе `make config` должна быть только сеть `backend` и одна публикация `127.0.0.1:8080`. Для второй копии задайте другие имена, порт и оба каталога. Оба каталога должны быть доступны для записи пользователям образов.

```bash
docker compose ls -a
docker ps -a
ls -ld data/elasticsearch data/kibana
make build
```

`make init` сохраняет существующий `.docker.env` и создаёт недостающие каталоги. Права на запись для другого UID он не назначает. В проверенных образах Elasticsearch работает с UID 1000 и основным GID 0, Kibana — с UID 1000, основным GID 1000 и дополнительной группой 0. В командах ниже указаны свежая копия с настройками по умолчанию и локальный Linux. Сначала сверьте пути в `make config`, эффективные UID/GID, владельца и отсутствие содержимого.

```bash
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-elasticsearch
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-kibana
id
ls -ldn data/elasticsearch data/kibana
find data/elasticsearch data/kibana -mindepth 1 -maxdepth 1 -print
```

Если UID образов отличается от UID владельца и не имеет нужных прав, владелец может выдать доступ только к этим двум новым пустым каталогам. Выполняйте следующий пример после проверки UID 1000 и точных путей. Для него нужны утилиты `setfacl` и `getfacl` и локальная файловая система с POSIX ACL. Если она их не поддерживает, согласуйте новый подходящий путь с владельцем. Существующие каталоги данных оставьте без изменений.

```bash
setfacl -m u:1000:rwx -- data/elasticsearch data/kibana
getfacl -- data/elasticsearch data/kibana
```

```bash
make up
```

После успешной HTTP-проверки Elasticsearch Compose запускает Kibana в фоне. Проверьте готовность Kibana через /api/status. При смене домена или порта измените адреса в примерах. [Kibana](http://kibana.local:8080) · [Elasticsearch](http://elastic.local:8080)

## Подключение и проверка готовности

Для браузера добавьте две записи в файл hosts на той ОС, где работает браузер: Linux/macOS `/etc/hosts`, Windows `C:\Windows\System32\drivers\etc\hosts` (потребуются соответствующие права). Для curl запись hosts не обязательна: `--resolve` направляет запрос на loopback с нужным Host.

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

Корневой ответ Elasticsearch содержит `version.number` и `cluster_name`; `_cluster/health` сообщает состояние. `green` означает доступность всех шардов, `yellow` на одном узле может означать неназначенные реплики, `red` требует диагностики. В ответе `_cat/plugins` должны присутствовать оба плагина. Kibana готова, когда `/api/status` показывает `status.overall.level: available`; до этого возможен 502/503. Затем откройте [Kibana](http://kibana.local:8080) и Dev Tools → Console.

[Диагностика запуска](troubleshooting.md) · [Практика поиска и анализа текста](search-lab.md)

## Исторические скриншоты

Сохранены исходные иллюстрации раннего стенда (Elasticsearch 6.8.0). Внешний вид, меню и ответы современных версий отличаются; эти изображения не подтверждают текущий запуск.

![Elasticsearch 6.8.0 — корневой ответ](../../../assets/elastic-local-1.png)

![Elasticsearch 6.8.0 — ответ на поиск](../../../assets/elastic-local-2.png)

![Kibana — обзор кластера](../../../assets/kibana-local-1.png)

![Kibana — просмотр документов в Discover](../../../assets/kibana-local-2.png)

![Kibana — консоль Dev Tools](../../../assets/kibana-local-3.png)

## Документация

- [Практика поиска и анализа текста](search-lab.md)
- [Эксплуатация и Make-команды](operations.md)
- [Диагностика](troubleshooting.md)
- [Архитектура и конфигурация](../reference/configuration.md)
- [Участие в разработке](../../../../.github/CONTRIBUTING.md)
