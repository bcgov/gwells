#!/bin/bash -x

#create the database
psql --dbname postgres -h 127.0.0.1 --username ${DATABASE_USER} --command "CREATE DATABASE gwells WITH owner=\"${DATABASE_USER}\"" &&

#add a namespace for the gwells tables
psql -h 127.0.0.1 --username ${DATABASE_USER} --dbname ${DATABASE_NAME} --command "CREATE SCHEMA gwells" &&

#create the structure for the gwells tables
python ../../manage.py migrate

#add a namespace for the legacy wells tables
psql -h 127.0.0.1 --username ${DATABASE_USER} --dbname ${DATABASE_NAME} --command "CREATE SCHEMA wells" &&
read -p "path to wells dump:" wellsdump

eval wellsdump=$wellsdump

pg_restore --no-owner --dbname gwells --username ${DATABASE_USER} $wellsdump

#add the replication stored functions in the public schema
psql -h 127.0.0.1 --username ${DATABASE_USER} --dbname ${DATABASE_NAME} --file data-replication.sql
