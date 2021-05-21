FROM redis:6.0.6-alpine

COPY ./docker/dev/redis/redis.conf /var/lib/redis/redis.conf:ro

CMD ["redis-server", "/var/lib/redis/redis.conf:ro"]
