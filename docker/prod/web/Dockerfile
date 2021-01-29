###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.1-alpine as builder

# set work directory
WORKDIR /usr/src/web

RUN apk update \
	# install psycopg2 dependencies
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # install openssl dependencies
    && apk add openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev \
	&& pip install --upgrade pip

# install dependencies
COPY ./web/src/requirements  /usr/src/web/requirements
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/web/wheels -r /usr/src/web/requirements/production.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.0-alpine

# create the app user

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kyiv \
	LANG=C.UTF-8 \
	APP_HOME=/home/ubuntu/web

RUN mkdir -p $APP_HOME && addgroup -S ubuntu && adduser -S ubuntu -G ubuntu

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
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./docker/prod/web/entrypoint.sh /entrypoint.sh
COPY ./web $APP_HOME

RUN flake8 --ignore=E501,F401,F403,W504 .
# chown all the files to the www user
RUN chown -R ubuntu:ubuntu $APP_HOME && chown -R ubuntu:ubuntu /entrypoint.sh && chmod +x /entrypoint.sh

## change to the www user
#USER ubuntu
