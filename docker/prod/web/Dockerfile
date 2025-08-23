ARG PYTHON_VERSION=3.13
ARG WHEELS_PATH=/wheels
FROM python:${PYTHON_VERSION}-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Europe/Kyiv \
    LANG=C.UTF-8 \
    WORK_DIR=/app \
    DJANGO_SETTINGS_MODULE=src.settings

RUN apk add --update --no-cache --virtual .build-deps \
    build-base postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev && \
    pip install --upgrade pip


FROM base AS builder
ARG WHEELS_PATH

WORKDIR ${WORK_DIR}

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --upgrade poetry setuptools && \
    poetry self add poetry-plugin-export

COPY ["./web/pyproject.toml", "./web/poetry.lock", "./"]

RUN poetry export -f requirements.txt --without-hashes --without dev --with prod -o requirements.txt && \
    pip wheel --wheel-dir=${WHEELS_PATH} -r requirements.txt

# ================= RUNTIME =================
FROM base AS runtime

ARG PYTHON_VERSION
ARG WHEELS_PATH

ARG GID=1000
ARG UID=1000
ARG NGINX_GID=101
ARG USER=django

RUN apk add --update --no-cache --virtual .build-deps postgresql-dev curl nginx && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

WORKDIR ${WORK_DIR}
COPY --chown=$USER:$USER ./docker/prod/web/entrypoint.sh /
COPY ./docker/prod/nginx/ /etc/nginx/

COPY --from=builder ${WHEELS_PATH} ${WHEELS_PATH}
RUN pip install --no-build-isolation --no-cache-dir --no-index --find-links=${WHEELS_PATH} ${WHEELS_PATH}/* && \
    rm -rf ${WHEELS_PATH}

COPY ./web .

RUN chown -R $USER:$USER /etc/nginx /var/lib/nginx/ /var/log /run/nginx/ && \
    chmod +x /entrypoint.sh && \
    mkdir -p /gunicorn_socket && \
    chown $USER:$NGINX_GID /gunicorn_socket && \
    chmod 770 /gunicorn_socket && \
    python manage.py collectstatic --no-input

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

USER $USER
