FROM postgis/postgis:14-3.5-alpine

COPY ./initdb.sh /docker-entrypoint-initdb.d/init-user-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh