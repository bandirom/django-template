###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.1-alpine as builder

# set work directory
WORKDIR /usr/src/web

RUN apk update \
	  # install psycopg2 dependencies
    && apk add postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

# install dependencies
COPY ./web/src/requirements  /usr/src/web/requirements
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/web/wheels -r /usr/src/web/requirements/production.txt


#########
# FINAL #
#########

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


RUN apk update \
    && apk add --no-cache postgresql-dev curl gcc python3-dev musl-dev openssl libffi-dev openssl-dev build-base \
    # install Pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev \
    && addgroup -g $GID -S $USER \
    && adduser -S $USER -G $USER --disabled-password --uid "$UID"

WORKDIR $APP_HOME

COPY --from=builder /usr/src/web/wheels /wheels
COPY --chown=$USER:$USER --from=builder /usr/src/web/requirements $APP_HOME/requirements
RUN pip install --no-cache /wheels/*

COPY --chown=$USER:$USER ./docker/prod/web/entrypoint.sh /entrypoint.sh
COPY --chown=$USER:$USER ./web $APP_HOME

RUN chmod +x /entrypoint.sh && mkdir -p static && chown -R $USER:$USER static

RUN flake8 .

USER $USER
