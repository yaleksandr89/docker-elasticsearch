# Используем официальный образ Nginx
ARG NGINX_VERSION=latest
FROM nginx:${NGINX_VERSION}

# Указываем переменные окружения для подстановки
ARG ELASTIC_CONTAINER
ARG KIBANA_CONTAINER
ARG ELASTIC_PORT
ARG KIBANA_PORT
ARG ELASTIC_DOMAIN
ARG KIBANA_DOMAIN

# Копируем шаблон конфигурации внутрь контейнера
COPY default.conf.template /etc/nginx/conf.d/default.conf.template

# Устанавливаем envsubst для подстановки переменных
RUN apt-get update && apt-get install -y gettext-base && apt-get clean

# Подставляем переменные в шаблон и сохраняем итоговый конфиг
RUN envsubst '\$ELASTIC_CONTAINER \$KIBANA_CONTAINER \$ELASTIC_PORT \$KIBANA_PORT \$ELASTIC_DOMAIN \$KIBANA_DOMAIN' \
    < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Указываем, что Nginx будет работать в режиме "foreground"
CMD ["nginx", "-g", "daemon off;"]
