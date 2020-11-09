###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.0-alpine as builder

# set work directory
WORKDIR /usr/src/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kyiv \
	LANG=C.UTF-8

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # install openssl dependencies
    && apk add openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

# install dependencies
COPY ./web/src/requirements  /usr/src/web/requirements
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/web/wheels -r /usr/src/web/requirements/production.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.0-alpine

# create directory for the app user
RUN mkdir -p /home/www

# create the app user
RUN addgroup -S www && adduser -S www -G www

# create the appropriate directories
ENV APP_HOME /home/www/web
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # install openssl dependencies
    && apk add openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

COPY --from=builder /usr/src/web/wheels /wheels
COPY --from=builder /usr/src/web/requirements $APP_HOME/requirements
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./docker/prod/web/entrypoint.sh /entrypoint.sh

# copy project
COPY ./web $APP_HOME

RUN pip install flake8

RUN flake8 --ignore=E501,F401,F403,W504 .
# chown all the files to the www user
RUN chown -R www:www $APP_HOME
RUN chown -R www:www /entrypoint.sh

RUN chmod +x /entrypoint.sh

## change to the www user
#USER www
