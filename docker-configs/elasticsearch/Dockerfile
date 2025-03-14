# ARG позволяет передавать версию Elastic из docker-compose.yml
ARG ELASTIC_VERSION=lates

# Берем официальный образ Elasticsearch (Нужен VPN!)
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}

# Копируем конфигурационный файл внутрь контейнера
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

# Копируем файл с синонимами внутрь контейнера
# COPY synonyms.txt /usr/share/elasticsearch/config/analysis/synonyms.txt

# Проверяем, установлен ли плагин analysis-icu. Если плагин не установлен — ставим его.
RUN if [ ! -d "/usr/share/elasticsearch/plugins/analysis-icu" ]; then \
      elasticsearch-plugin install analysis-icu --batch; \
    fi

# Проверяем, установлен ли плагин analysis-phonetic. Если плагин не установлен — ставим его.
RUN if [ ! -d "/usr/share/elasticsearch/plugins/analysis-phonetic" ]; then \
      elasticsearch-plugin install analysis-phonetic --batch; \
    fi
