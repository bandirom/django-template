# pull official base image
FROM python:3.9.1-alpine
MAINTAINER bandirom@ukr.net

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kiev \
	LANG=C.UTF-8 \
	HOME=/usr/src/web

WORKDIR $HOME

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev build-base \
    # install Pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev \
	&& pip install --upgrade pip

COPY ./web/src/requirements  ./requirements
RUN pip install -r ./requirements/local.txt

COPY ./docker/dev/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./web $HOME
