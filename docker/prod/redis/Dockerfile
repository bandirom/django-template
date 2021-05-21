FROM redis:6.0.6-alpine

COPY ./docker/prod/redis/redis.conf /var/lib/redis/redis.conf:ro

CMD ["redis-server", "/var/lib/redis/redis.conf:ro"]
