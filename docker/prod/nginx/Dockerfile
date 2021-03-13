FROM nginx:1.19.7

ENV	TZ=Europe/Kiev
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/conf.d/ /etc/nginx/conf.d/
