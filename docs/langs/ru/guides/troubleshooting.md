# Диагностика

## Выберите язык

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| **Выбран** | [English](../../en/guides/troubleshooting.md) | [Español](../../es/guides/troubleshooting.md) | [中文](../../zh/guides/troubleshooting.md) | [Français](../../fr/guides/troubleshooting.md) | [Deutsch](../../de/guides/troubleshooting.md) |

Начните с итоговой конфигурации, состояния и журналов. Перед публикацией вывода удалите пароли, токены, данные и внутренние имена. Команды ниже для локального режима. В режиме интеграции добавьте `WITH_EXTERNAL_NETWORK=1` к вызовам Make и `-f docker-compose.external.yml` к вызову Compose.

[Начало работы](getting-started.md)

```bash
make config
docker compose --env-file .docker.env -f docker-compose.yml ps -a
make log elasticsearch
make log kibana
make log nginx
```

## Ошибка внешней сети

Ошибка отсутствующей внешней сети возможна только при явном подключении. Сравните имя из `EXTERNAL_NETWORK` с результатом `docker network ls`, затем выполните `docker network inspect` с фактическим именем. Сверьте её участников с владельцем приложения. Чужие сети не создавайте, не меняйте и не удаляйте. Ниже исторический снимок версии 6.8.

```bash
docker network ls
```

![Ошибка внешней сети](../../../assets/make-up-error.png) (6.8)

## Порты, домены и 502/503

Если порт занят, выберите свободный `NGINX_PORT` и обновите все URL и аргументы `--resolve`. Внутренние порты 9200 и 5601 фиксированы. Если curl работает, а браузер нет, проверьте файл hosts на машине браузера и обход прокси для обоих доменов. Неизвестный Host получает HTTP 404. При 502/503 посмотрите состояние и журналы upstream: Compose ждёт ограниченную по времени HTTP-проверку Elasticsearch, а Kibana готова при `status.overall.level: available` из `/api/status`. Если проверка Elasticsearch исчерпана, сначала устраните причину в его журнале. Применяйте изменения через `make build` для образов и `make up` для конфигурации либо через `down` и `up` с прежними путями данных. Один `restart` изменений не применит.

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

## Сборка, плагины и ресурсы

При ошибке сборки проверьте доступ к официальным реестрам и загрузке плагинов. Версии Elasticsearch и Kibana должны совпадать, а `_cat/plugins` должен показывать `analysis-icu` и `analysis-phonetic` той же версии. Для ошибок запуска проверьте свободное место, память Docker, сообщения об OOM, `vm.max_map_count` и [права обоих UID/GID](getting-started.md) на фактические каталоги. При ошибке анализатора прочтите ответ API и проверьте `config/analysis/synonyms.txt`. Исправляйте причину ошибки, не скрывайте неверные правила параметром `lenient`.

## Документация

- [Начало работы](getting-started.md)
- [Практика поиска и анализа текста](search-lab.md)
- [Эксплуатация и Make-команды](operations.md)
- [Архитектура и конфигурация](../reference/configuration.md)
- [Участие в разработке](../../../../.github/CONTRIBUTING.md)
