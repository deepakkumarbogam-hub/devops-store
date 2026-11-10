FROM nginxinc/nginx-unprivileged:alpine

COPY --chown=101:101 frontend/frontend/index.html /usr/share/nginx/html/index.html
COPY --chown=101:101 frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
