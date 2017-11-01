#!/bin/bash -x
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# to make conventient use of this script in ##development## edit your pg_hba.conf file to set users to be trusted locally
# https://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

#collect authentication credentials for process

#get name of Superuser who will run the replication -- a superuser is necessary to install the extension which is used to create guids
# -p is for prompt
read -p "Superuser that will run the replication: " superuser &&

#get the password for the Superuser who will run the replication
# -p is for prompt
#read -s -p "Enter the password for DB Superuser - $superuser: " superuser_password &&
#newline
#echo -e ""

#get the password for the owner of ${DATABASE_NAME}
# -p is for prompt
# -s to hide password as it is entered
#read -s -p "Password for DB User - ${DATABASE_USER}: " password &&
#newline
#echo -e ""

#get path to legacy data .dmp
# -p is for prompt
#read -p "path to wells dump: " wellsdump &&
#eval wellsdump=$wellsdump &&
eval wellsdump=${BACKUP_LOCATION}

#recreate the database
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/postgres <<EOF
DROP DATABASE IF EXISTS ${DATABASE_NAME};
DROP SCHEMA IF EXISTS ${LEGACY_DATABASE_SCHEMA};
CREATE DATABASE ${DATABASE_NAME} WITH owner=${DATABASE_USER};
EOF

#set search_path
#add replication functions to the public schema
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/${DATABASE_NAME} <<EOF
ALTER USER ${DATABASE_USER} SET search_path TO public;
\include clear-tables.sql
\include create-xform-gwells-well-ETL-table.sql
\include copy-remote-code-tables.sql
\include populate-xform-gwells-well.sql
\include populate-gwells-from-xform.sql
\include setup-replicate.sql
\include replicate.sql
EOF

#restore the legacy data - superuser necessary because of ownership issues
pg_restore --dbname postgresql://${DATABASE_USER}:${DATABASE_USER}@127.0.0.1:5432/${DATABASE_NAME} --no-owner $wellsdump

#clean up permissions just in case
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
REVOKE ALL ON SCHEMA public FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA public TO ${DATABASE_USER};
REVOKE ALL ON SCHEMA public FROM ${LEGACY_DATABASE_SCHEMA};
GRANT ALL ON SCHEMA public TO ${LEGACY_DATABASE_SCHEMA};
EOF

#create the structure for the gwells tables
python ../../manage.py makemigrations
python ../../manage.py migrate


#install crypto extension to support UUID creation
#setup replication -- superuser must setup replication because it uses the COPY command
psql --dbname postgresql://$superuser:$superuser}@127.0.0.1:5432/${DATABASE_NAME}<<EOF
DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;
SELECT public.setup_replicate();
EOF

#setup replication
#replicate
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER}@127.0.0.1:5432/${DATABASE_NAME}<<EOF
SELECT public.replicate();
EOF
