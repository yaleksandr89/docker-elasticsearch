# ARG позволяет передавать версию Elastic из docker-compose.yml
ARG ELASTIC_VERSION

# Берем официальный образ Elasticsearch (Нужен VPN!)
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}


# Копируем конфигурационный файл внутрь контейнера
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

# Проверяем, установлен ли плагин analysis-icu.
# Если плагин не установлен — ставим его.
RUN if [ ! -d "/usr/share/elasticsearch/plugins/analysis-icu" ]; then \
      elasticsearch-plugin install analysis-icu --batch; \
    fi \
