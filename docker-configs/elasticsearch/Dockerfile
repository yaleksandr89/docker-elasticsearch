ARG ELASTIC_VERSION=9.5.7
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}

COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY synonyms.txt /usr/share/elasticsearch/config/analysis/synonyms.txt
RUN elasticsearch-plugin install --batch analysis-icu analysis-phonetic
