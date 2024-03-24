FROM nginx:1.25-alpine
WORKDIR /opt/ct_web

# Context is assigned to apps's root
ADD ./webapps/telegram/dist /opt/ct_web/tg
ADD ./docker/web.conf /etc/nginx/conf.d/default.conf
