# ARG позволяет передавать версию Kibana из docker-compose.yml
ARG KIBANA_VERSION=lates

# Берем официальный образ Kibana (Нужен VPN!)
FROM docker.elastic.co/kibana/kibana:${KIBANA_VERSION}

# Переключаемся на пользователя root для изменения прав
USER root

# Устанавливаем envsubst для подстановки переменных
RUN apt-get update && apt-get install -y gettext-base && apt-get clean

# Копируем шаблонный конфиг Kibana
COPY kibana.yml.template /usr/share/kibana/config/kibana.yml.template

# Копируем объединённый скрипт для генерации конфига и старта Kibana
COPY start-kibana.sh /usr/local/bin/start-kibana.sh

# Даем права на выполнение скрипта
RUN chmod +x /usr/local/bin/start-kibana.sh

# Переключаемся обратно на пользователя kibana
USER kibana

# Запуск скрипта при старте контейнера
CMD ["/usr/local/bin/start-kibana.sh"]
