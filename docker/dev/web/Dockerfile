FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kyiv \
    LANG=C.UTF-8 \
    WORK_DIR=/app \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DJANGO_SETTINGS_MODULE=src.settings

WORKDIR ${WORK_DIR}

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apk add --update --no-cache curl libpq jpeg zlib openjpeg lcms2 tiff harfbuzz fribidi && \
    pip install --upgrade pip poetry setuptools && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID" && \
    mkdir -p /var/run/celery && \
    chown -R $USER:$USER /var/run/celery

COPY ./web/pyproject.toml ./web/poetry.lock ./

RUN poetry install --with dev --no-ansi

COPY --chown=$USER:$USER ./docker/dev/web/entrypoint.sh /
COPY --chown=$USER:$USER ./web ${WORK_DIR}

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

USER $USER
