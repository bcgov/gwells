FROM postgis/postgis:12-3.0

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main 9.6" > /etc/apt/sources.list.d/pgdg.list; \
			apt-get update; \
      apt-get -y --no-install-recommends install postgresql-9.6=9.6.17-2.pgdg90+1 postgresql-contrib-9.6=9.6.17-2.pgdg90+1
