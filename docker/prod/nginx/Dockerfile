FROM nginx:1.19.7

ARG HOME=/etc/nginx
ENV	TZ=Europe/Kiev

WORKDIR $HOME
RUN rm $HOME/conf.d/default.conf

COPY ./docker/prod/nginx/nginx.conf $HOME
COPY ./docker/prod/nginx/conf.d/ $HOME/conf.d/
