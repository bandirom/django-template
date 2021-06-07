FROM postgres:12.6-alpine

COPY docker/dev/db/pg.conf /etc/postgresql/postgresql.conf
RUN mkdir -p /postgres_socket && chown -R postgres:postgres /postgres_socket
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]

