# pull official base image
FROM python:3.9.1-alpine as builder
MAINTAINER bandirom@ukr.net

RUN apk update \
	  # install psycopg2 dependencies
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

ARG TEMP_PATH=/usr/src/web

# install dependencies
COPY ./web/src/requirements  $TEMP_PATH/requirements

RUN pip install --upgrade pip \
  && pip install --no-warn-script-location --prefix=/install -r $TEMP_PATH/requirements/production.txt


# pull official base image
FROM python:3.9.1-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kiev \
	LANG=C.UTF-8 \
	APP_HOME=/home/ubuntu/web

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu


RUN apk update && apk add --no-cache postgresql-dev curl \
    && addgroup -g $GID -S $USER \
    && adduser -S $USER -G $USER --disabled-password --uid "$UID" \
    && mkdir -p /gunicorn_socket /redis_socket \
    && chmod -R 777 /gunicorn_socket /redis_socket \
    && chown -R $USER:$USER /gunicorn_socket

WORKDIR $APP_HOME

COPY --from=builder /install /usr/local
COPY --chown=$USER:$USER ./docker/prod/web/entrypoints /
COPY --chown=$USER:$USER ./web $APP_HOME

RUN chmod +x /*.sh \
    && mkdir -p static logs \
    && chown -R $USER:$USER static logs \
    && flake8 .

USER $USER
