#!/bin/bash
set -e

# Выполняем подстановку только нужных переменных
echo "💥 Выполняется замена переменных в конфиге Nginx..."
envsubst '$ELASTIC_DOMAIN $ELASTIC_CONTAINER $ELASTIC_PORT $KIBANA_DOMAIN $KIBANA_CONTAINER $KIBANA_PORT' < /etc/nginx/conf.d/default.conf.template | sed 's/__/$/g' > /etc/nginx/conf.d/default.conf

# Выводим результат для проверки
cat /etc/nginx/conf.d/default.conf

# Запускаем Nginx
echo "✅ Запуск Nginx..."
exec nginx -g "daemon off;"
