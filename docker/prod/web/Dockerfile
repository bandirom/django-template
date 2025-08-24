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

# Minimal runtime libraries required for Django & Pillow
RUN apk add --update --no-cache \
    libpq jpeg zlib openjpeg lcms2 tiff harfbuzz fribidi curl nginx

# ================================= BUILDER =================================
FROM base AS builder
WORKDIR ${WORK_DIR}
ARG WHEELS_PATH

# Build dependencies for compiling wheels
RUN apk add --update --no-cache --virtual .build-deps \
    build-base postgresql-dev gcc python3-dev musl-dev \
    openssl-dev libffi-dev jpeg-dev zlib-dev lcms2-dev \
    openjpeg-dev tiff-dev

VOLUME ${WHEELS_PATH}

# Install Poetry and export plugin
RUN pip install --upgrade pip poetry setuptools && \
    poetry self add poetry-plugin-export

COPY ./web/pyproject.toml ./web/poetry.lock ./

# Export requirements and build wheel files
RUN poetry export -f requirements.txt --without-hashes --without dev --with prod -o requirements.txt && \
    pip wheel --wheel-dir=${WHEELS_PATH} -r requirements.txt

# ================================= RUNTIME =================================
FROM base AS runtime
ARG WHEELS_PATH

ARG GID=1000
ARG UID=1000
ARG NGINX_GID=101
ARG USER=django

RUN addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

WORKDIR ${WORK_DIR}

COPY --chown=$USER:$USER ./docker/prod/web/entrypoint.sh /
COPY ./docker/prod/nginx/ /etc/nginx/

# Copy wheels and requirements from builder
COPY --from=builder ${WHEELS_PATH} ${WHEELS_PATH}
COPY --from=builder ${WORK_DIR}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=${WHEELS_PATH} -r requirements.txt && \
    rm -rf ${WHEELS_PATH} /root/.cache/pip requirements.txt

COPY ./web .

# Set permissions and prepare Gunicorn socket
RUN chown -R $USER:$USER /etc/nginx /var/lib/nginx/ /var/log /run/nginx/ && \
    chmod +x /entrypoint.sh && \
    mkdir -p /gunicorn_socket /var/run/celery && \
    chown $USER:$NGINX_GID /gunicorn_socket && \
    chown -R $USER:$USER /var/run/celery && \
    chmod 770 /gunicorn_socket && \
    python manage.py collectstatic --no-input

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

USER $USER
