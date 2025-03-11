#!/bin/bash

# Скрипт завершится, если команда вернет ошибку
set -e

ELASTIC_URL="http://${ELASTICSEARCH_URL}"

echo "⏳ Ожидание доступности Elasticsearch по адресу $ELASTIC_URL..."

# Бесконечный цикл проверки
until curl -s "$ELASTIC_URL" | grep -q 'cluster_name'; do
  echo "🔄 Elasticsearch еще не готов. Ждем 5 секунд..."
  sleep 5
done

echo "✅ Elasticsearch доступен. Запуск Kibana..."

# Запуск Kibana
exec /usr/local/bin/kibana-docker
