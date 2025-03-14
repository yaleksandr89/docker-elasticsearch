#!/bin/bash
set -e

# Формируем конфиг Kibana из шаблона
echo "💥 Выполняется замена переменных в конфиге Kibana..."
envsubst < /usr/share/kibana/config/kibana.yml.template > /usr/share/kibana/config/kibana.yml
cat /usr/share/kibana/config/kibana.yml

# Ожидаем доступность Elasticsearch
ELASTIC_URL="${ELASTICSEARCH_HOSTS}"
echo "⏳ Проверяем доступность Elasticsearch по адресу: $ELASTIC_URL"

until curl -s "$ELASTIC_URL" | grep -q 'cluster_name'; do
  echo "🔄 Elasticsearch не доступен. Повторяем попытку через 5 секунд..."
  sleep 5
done

echo "✅ Elasticsearch доступен. Запуск Kibana..."

# Запускаем Kibana
exec /usr/local/bin/kibana-docker
