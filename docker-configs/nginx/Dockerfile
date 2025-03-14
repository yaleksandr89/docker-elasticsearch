# Используем официальный образ Nginx
ARG NGINX_VERSION=latest
FROM nginx:${NGINX_VERSION}

# Копируем шаблон конфигурации внутрь контейнера
COPY default.conf.template /etc/nginx/conf.d/default.conf.template

# Копируем скрипт для замены переменных и запуска Nginx
COPY start-nginx.sh /usr/local/bin/start-nginx.sh

# Даем права на выполнение скрипта
RUN chmod +x /usr/local/bin/start-nginx.sh

# Устанавливаем envsubst для подстановки переменных
RUN apt-get update && apt-get install -y gettext-base && apt-get clean

# Указываем команду для выполнения скрипта при запуске контейнера
CMD ["/usr/local/bin/start-nginx.sh"]
