ARG PYTHON_VERSION=3.13
ARG WORK_DIR=/app

FROM python:${PYTHON_VERSION}-alpine AS builder
ARG WORK_DIR

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1

WORKDIR ${WORK_DIR}

RUN apk add --update --no-cache --virtual .build-deps \
    build-base postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev && \
    pip install --upgrade poetry setuptools

COPY ["./web/pyproject.toml", "./web/poetry.lock", "./"]

RUN poetry install --with prod

FROM python:${PYTHON_VERSION}-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kiev \
    LANG=C.UTF-8 \
    DJANGO_SETTINGS_MODULE=src.settings

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu
ARG PYTHON_VERSION
ARG WORK_DIR

RUN apk add --update --no-cache --virtual .build-deps postgresql-dev curl nginx && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"
# && \
 #    mkdir -p /gunicorn_socket /redis_socket && \
 #    chmod -R 777 /gunicorn_socket /redis_socket && \
 #    chown -R $USER:$USER /gunicorn_socket

WORKDIR ${WORK_DIR}

COPY --from=builder /app/dist /wheels
RUN pip install --no-index --find-links=/wheels *.whl

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "src.asgi:application"]

EXPOSE 8000

USER $USER
