ARG NGINX_VERSION=1.30.8-trixie
FROM nginx:${NGINX_VERSION}

ENV NGINX_ENVSUBST_FILTER="^(ELASTIC|KIBANA)_(DOMAIN|PORT)$"
COPY default.conf.template /etc/nginx/templates/default.conf.template
COPY --chmod=755 start-nginx.sh /docker-entrypoint.d/15-check-routing.sh
