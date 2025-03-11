# ARG позволяет передавать версию Kibana из docker-compose.yml
ARG KIBANA_VERSION=lates

# Берем официальный образ Kibana (Нужен VPN!)
FROM docker.elastic.co/kibana/kibana:${KIBANA_VERSION}

# Копируем конфигурационный файл внутрь контейнера
COPY kibana.yml /usr/share/kibana/config/kibana.yml

# Копируем скрипт, который ждет запуск Elasticsearch перед стартом Kibana
COPY wait-for-elastic.sh /usr/local/bin/wait-for-elastic.sh

# Переключаемся на пользователя root для изменения прав
USER root

# Даем права на выполнение скрипта
RUN chmod +x /usr/local/bin/wait-for-elastic.sh

# Переключаемся обратно на пользователя kibana
USER kibana

CMD ["/usr/local/bin/wait-for-elastic.sh"]
