FROM gitlab/gitlab-runner:latest
ENV COMPOSE_VERSION=1.28.6 \
    TZ=Europe/Kiev


RUN curl -sSL https://get.docker.com/ | sh \
    && curl -L https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose
