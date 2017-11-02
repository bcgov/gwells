#!/bin/bash -x
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# to make conventient use of this script in ##development## edit your pg_hba.conf file to set users to be trusted locally
# https://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

#get path to legacy data .dmp
# -p is for prompt
#read -p "path to wells dump: " wellsdump &&
#eval wellsdump=$wellsdump &&
eval wellsdump=${BACKUP_LOCATION} &&

#get name of Superuser who will run the replication -- a superuser is necessary
#to install the pgcrypto extension which is used to create guids
# -p is for prompt
read -p "Superuser that will configure template1 to provide pgcrytpo: " superuser &&

#get the password for the Superuser who will run the replication - needed if pg_hba.conf not configured
# -p is for prompt
read -s -p "Enter the password for DB Superuser - $superuser: " superuser_password &&
#newline
echo -e ""


###ENVIRONMENT CONFIG###
#configure pgcrypto extension so that GUIDs can be created in all new databases
#configure postgres_fdw extension so that we can remotely collect legacy data
#drop user dependencies - it is assumed that the only dependencies are the
#expected owned datbases and their respective tables
#configure legacy and novel users
psql --echo-queries --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/postgres <<EOF
\c template1
DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;
DROP EXTENSION IF EXISTS postgres_fdw;
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

\c postgres
DROP DATABASE IF EXISTS ${DATABASE_NAME};
DROP USER IF EXISTS ${DATABASE_USER};
CREATE USER ${DATABASE_USER} WITH CREATEDB;
ALTER USER ${DATABASE_USER} WITH ENCRYPTED PASSWORD '${DATABASE_USER_PASSWORD}';
ALTER USER ${DATABASE_USER} SET search_path TO public;

DROP DATABASE IF EXISTS ${LEGACY_DATABASE_NAME};
DROP USER IF EXISTS ${LEGACY_DATABASE_USER};
CREATE USER ${LEGACY_DATABASE_USER} WITH CREATEDB;
ALTER USER ${LEGACY_DATABASE_USER} WITH ENCRYPTED PASSWORD '${LEGACY_DATABASE_USER_PASSWORD}';
ALTER USER ${LEGACY_DATABASE_USER} SET search_path TO public;
EOF

#drop/create/connect novel database
#refresh public schema permissions
#set search path
#add the stored procedures required for replication
#create the legacy schema for the FDW tables
#refresh the permissions on the legacy schema
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/postgres <<EOF

CREATE DATABASE ${DATABASE_NAME};
\c ${DATABASE_NAME}
REVOKE ALL ON SCHEMA public FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA public TO ${DATABASE_USER};

\include clear-tables.sql
\include create-xform-gwells-well-ETL-table.sql
\include copy-remote-code-tables.sql
\include populate-xform-gwells-well.sql
\include populate-gwells-from-xform.sql
\include setup-replicate.sql
\include replicate.sql

CREATE SCHEMA ${LEGACY_DATABASE_SCHEMA};
REVOKE ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
EOF

#drop/create/connect the legacy database
#refresh public schema permissions
psql --dbname postgresql://${LEGACY_DATABASE_USER}:${LEGACY_DATABASE_USER_PASSWORD}@127.0.0.1:5432/postgres <<EOF

DROP DATABASE IF EXISTS ${LEGACY_DATABASE_NAME};
CREATE DATABASE ${LEGACY_DATABASE_NAME};

\c ${LEGACY_DATABASE_NAME}

REVOKE ALL ON SCHEMA public FROM ${LEGACY_DATABASE_USER};
GRANT ALL ON SCHEMA public TO ${LEGACY_DATABASE_USER};

EOF

#restore the legacy data
pg_restore --dbname postgresql://${LEGACY_DATABASE_USER}:${LEGACY_DATABASE_USER_PASSWORD}@127.0.0.1:5432/${LEGACY_DATABASE_NAME} --no-owner --no-privileges $wellsdump

#refresh legacy schema permissions
psql --dbname postgresql://${LEGACY_DATABASE_USER}:${LEGACY_DATABASE_USER_PASSWORD}@127.0.0.1:5432/${LEGACY_DATABASE_NAME} <<EOF
REVOKE ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM ${LEGACY_DATABASE_USER};
GRANT ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${LEGACY_DATABASE_USER};
EOF

#create the structure for the gwells tables
python ../../manage.py makemigrations
python ../../manage.py migrate

#create foreign data wrapper to legacy database
#superuser is required because of ownership limitations with the FDW
#superuser is required for copy command which is used by setup_replicate
psql --echo-queries --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME}<<EOF
DROP SERVER IF EXISTS ${LEGACY_DATABASE_NAME} CASCADE;
CREATE SERVER ${LEGACY_DATABASE_NAME} FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'localhost', dbname '${LEGACY_DATABASE_NAME}');
DROP USER MAPPING IF EXISTS FOR PUBLIC SERVER ${LEGACY_DATABASE_NAME};
CREATE USER MAPPING FOR PUBLIC SERVER ${LEGACY_DATABASE_NAME} OPTIONS (user '${LEGACY_DATABASE_USER}', password '${LEGACY_DATABASE_USER_PASSWORD}');
IMPORT FOREIGN SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM SERVER ${LEGACY_DATABASE_NAME} INTO ${LEGACY_DATABASE_SCHEMA};
GRANT USAGE ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
GRANT SELECT ON ALL TABLES IN SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
GRANT USAGE ON FOREIGN SERVER ${LEGACY_DATABASE_NAME} TO ${DATABASE_USER};

SELECT public.setup_replicate();
EOF

#replicate
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
SELECT public.replicate();
EOF
