FROM nginx:1.18.0-alpine

ENV	TZ=Europe/Kiev
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/conf.d/ /etc/nginx/conf.d/
