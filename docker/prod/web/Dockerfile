FROM python:3.11-alpine3.15 as builder
ARG WHEELS_PATH=/etc/wheels

RUN apk add --update --no-cache --virtual .build-deps \
    build-base postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    # install Pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

COPY ./web/setup.cfg ./web/pyproject.toml ./
COPY ./web/src/requirements  ./src/requirements

RUN pip wheel --wheel-dir=$WHEELS_PATH .[production]


FROM python:3.11-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kiev \
    LANG=C.UTF-8 \
    APP_HOME=/web

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu
ARG WHEELS_PATH=/etc/wheels

RUN apk add --update --no-cache --virtual .build-deps postgresql-dev curl nginx && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID" && \
    mkdir -p /gunicorn_socket /redis_socket && \
    chmod -R 777 /gunicorn_socket /redis_socket && \
    chown -R $USER:$USER /gunicorn_socket

WORKDIR $APP_HOME

COPY --from=builder $WHEELS_PATH $WHEELS_PATH
COPY ./web/setup.cfg ./web/pyproject.toml ./
COPY ./web/src/requirements  ./src/requirements
RUN pip install --no-build-isolation --no-index --find-links=$WHEELS_PATH --editable .[production] && \
    rm -rf $WHEELS_PATH

COPY --chown=$USER:$USER ./docker/prod/web/entrypoint.sh /
COPY ./docker/prod/nginx/conf.d /etc/nginx/conf.d
COPY ./docker/prod/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./web $APP_HOME

RUN chmod +x /*.sh && \
    mkdir -p media && \
    python manage.py collectstatic --no-input && \
    chown -R $USER:$USER $APP_HOME media && \
    chown -R $USER:$USER /etc/nginx /var/lib/nginx/ /var/log /run/nginx/

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "src.asgi:application"]

EXPOSE 8000

USER $USER
