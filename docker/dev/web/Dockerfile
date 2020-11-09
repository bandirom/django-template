# pull official base image
FROM python:3.9.0-alpine
MAINTAINER nazarii.romanchenko@stemsc.com

ENV HOME /usr/src/web
# set work directory
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kyiv \
	LANG=C.UTF-8

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev \
	&& pip install --upgrade pip

COPY ./web/src/requirements  ./requirements

RUN pip install -r ./requirements/local.txt
# copy entrypoint.sh
COPY ./docker/dev/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# copy project
COPY ./web /usr/src/web/
