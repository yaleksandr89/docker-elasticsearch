# Участие в разработке

## Выберите язык

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| **Выбран** | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/CONTRIBUTING.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/CONTRIBUTING.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/CONTRIBUTING.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/CONTRIBUTING.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/CONTRIBUTING.md) |

Сообщайте воспроизводимые ошибки через Issues, вопросы и идеи через Discussions. Не публикуйте реальные данные, локальные конфигурации, пароли и подробности уязвимостей. Для крупных изменений сначала согласуйте цель с владельцем.

- Воспроизводимые ошибки — [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues).
- Вопросы и идеи — [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions).

Сохраняйте Make-команды, имена параметров, совместимость данных и назначение стенда. Изменения образов, сети, публикации портов, auth/TLS и хранения требуют отдельного решения. Для проверок используйте новую копию с синтетическими данными и уникальными контейнерами, портом и проектом; не затрагивайте рабочий стенд.

## Проверки

CI запускается для push и pull request в `master`, а также вручную через Actions. `quality` проверяет синтаксис startup-скриптов, учебные fixtures и resolved Compose; `docker-smoke` собирает отдельный стенд на фиксированных версиях, проверяет HTTP через оба virtual host, плагины и учебный поиск. Факт успешного запуска подтверждают результаты CI, а не наличие workflow.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

По умолчанию `WITH_EXTERNAL_NETWORK=0`. Для интеграции укажите существующую доверенную сеть в `EXTERNAL_NETWORK` и передавайте `WITH_EXTERNAL_NETWORK=1` каждой Make-команде. Только Elasticsearch присоединится к ней. Её участники получают доступ без пароля по имени контейнера на порту 9200. Compose сохраняет эту сеть при остановке.

## Pull Request

Создайте тематическую ветку от `master`, используйте подписанные коммиты Conventional Commits с русским описанием. В PR укажите причину, изменение, влияние на данные и безопасность, фактические проверки. Синхронизируйте шесть локалей; не ослабляйте проверки ради зелёного CI.

## Документация

- [Начало работы](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/ru/guides/getting-started.md)
- [Практика поиска и анализа текста](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/ru/guides/search-lab.md)
- [Эксплуатация и Make-команды](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/ru/guides/operations.md)
- [Диагностика](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/ru/guides/troubleshooting.md)
- [Архитектура и конфигурация](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/ru/reference/configuration.md)
