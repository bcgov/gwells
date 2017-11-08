#!/bin/bash -x
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# to make conventient use of this script in ##development## edit your pg_hba.conf file to set users to be trusted locally
# https://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/postgres <<EOF

DROP DATABASE IF EXISTS ${DATABASE_NAME};
CREATE DATABASE ${DATABASE_NAME};

\c ${DATABASE_NAME}

DROP SCHEMA IF EXISTS ${LEGACY_DATABASE_SCHEMA};
CREATE SCHEMA ${LEGACY_DATABASE_SCHEMA};
REVOKE ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};

\include create-xform-gwells-well-ETL-table.sql
\include populate-xform-gwells-well.sql
\include populate-gwells-well-from-xform.sql

\include setup-replicate.sql
\include replicate.sql
EOF

read -p "superuser that will create the foreign data wrapper: " superuser
read -s -p "superuser's password: " superuser_password

#create foreign data wrapper to legacy database
#superuser is required because of ownership limitations with the FDW
psql --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME}<<EOF
DROP SERVER IF EXISTS ${LEGACY_DATABASE_NAME} CASCADE;
CREATE SERVER ${LEGACY_DATABASE_NAME} FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'localhost', dbname '${LEGACY_DATABASE_NAME}');
DROP USER MAPPING IF EXISTS FOR PUBLIC SERVER ${LEGACY_DATABASE_NAME};
CREATE USER MAPPING FOR PUBLIC SERVER ${LEGACY_DATABASE_NAME} OPTIONS (user '${LEGACY_DATABASE_USER}', password '${LEGACY_DATABASE_USER_PASSWORD}');
IMPORT FOREIGN SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM SERVER ${LEGACY_DATABASE_NAME} INTO ${LEGACY_DATABASE_SCHEMA};
GRANT USAGE ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
GRANT SELECT ON ALL TABLES IN SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
GRANT USAGE ON FOREIGN SERVER ${LEGACY_DATABASE_NAME} TO ${DATABASE_USER};
EOF

python ../../manage.py makemigrations
python ../../manage.py migrate

cd ../code-tables

#copy code tables
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
\include ../scripts/clear-tables.sql
\include data-load-static-codes.sql
EOF

cd ../scripts

#replicate
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
SELECT public.replicate();
\i migrate_screens.sql
EOF
