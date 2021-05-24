FROM redis:6.0.6-alpine

COPY ./docker/prod/redis/redis.conf /var/lib/redis/redis.conf:ro

RUN mkdir -p /redis_socket && chmod -R 777 /redis_socket

CMD ["redis-server", "/var/lib/redis/redis.conf:ro"]
