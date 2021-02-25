FROM nginx:1.18.0-alpine

ENV	TZ=Europe/Kiev
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/nginx.conf ./docker/prod/nginx/proxy.conf /etc/nginx/conf.d/

# If you need to push default images like profile avatar or smth else, use the command below
# COPY ./web/media/profiles/default.jpg /home/ubuntu/web/media/profiles/default.jpg
