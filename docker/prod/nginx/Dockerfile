FROM nginx:1.18.0-alpine

ENV HOME /home/www/web
WORKDIR $HOME
RUN mkdir -p $HOME/media/profiles/ && rm /etc/nginx/conf.d/default.conf

# If you need to push default images like profile avatar or smth else, use the command below
#COPY ./web/media/profiles/default.jpg $HOME/media/profiles/default.jpg

COPY ./docker/prod/nginx/nginx.conf /etc/nginx/conf.d
