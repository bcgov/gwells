#!/bin/bash
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

#collect authentication credentials for process

#get name of Superuser who will run the replication
# -p is for prompt
read -p "Superuser that will run the replication: " superuser &&
#newline

#get the password for the Superuser who will run the replication
# -p is for prompt
read -s -p "Enter the password for DB Superuser - $superuser: " superuser_password &&
#newline
echo -e ""

#get the password for the owner of ${DATABASE_NAME}
# -p is for prompt
# -s to hide password as it is entered
read -s -p "Password for DB User - ${DATABASE_USER}: " password &&
#newline
echo -e ""

#get path to legacy data .dmp
# -p is for prompt
read -p "path to wells dump: " wellsdump &&
eval wellsdump=$wellsdump &&

#recreate the database
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/postgres <<EOF
DROP DATABASE IF EXISTS gwells;
CREATE DATABASE gwells WITH owner=${DATABASE_USER};
EOF

#set search_path
#add replication functions to the public schema
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/${DATABASE_NAME} <<EOF
ALTER USER ${DATABASE_USER} SET search_path TO public;
\include data-replication.sql
EOF

#restore the legacy data - superuser necessary because of ownership issues
pg_restore --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME} --no-owner $wellsdump &&

#create ${DATABASE_SCHEMA} and ${LEGACY_DATABASE_SCHEMA}
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/${DATABASE_NAME} <<EOF
CREATE SCHEMA ${DATABASE_SCHEMA};
CREATE SCHEMA ${LEGACY_DATABASE_SCHEMA};
EOF

#clean up permissions just in case
psql --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME} <<EOF 
REVOKE ALL ON SCHEMA public FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA public TO ${DATABASE_USER};
REVOKE ALL ON SCHEMA ${DATABASE_SCHEMA} FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA ${DATABASE_SCHEMA} TO ${DATABASE_USER};
REVOKE ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA ${LEGACY_DATABASE_SCHEMA} TO ${DATABASE_USER};
EOF

#adjust the tablenames
gwellsRegex="^gw_"
wellsRegex="^wells_"
adjustTableNamesSql=""

#build the sql so that you only need one connection
#don't use a pipe because that creates a subshell and you'll lose your variable value
while read -r tablename; do
	if [[ ${tablename} =~ $gwellsRegex ]]; then
                adjustTableNamesSql+="ALTER TABLE ${tablename} OWNER TO ${DATABASE_USER};"
                adjustTableNamesSql+="ALTER TABLE ${tablename} SET SCHEMA ${DATABASE_SCHEMA};"
                adjustTableNamesSql+="ALTER TABLE ${DATABASE_SCHEMA}.${tablename} RENAME TO ${tablename:3};"
	fi
	if [[ ${tablename} =~ $wellsRegex ]]; then
                adjustTableNamesSql+="ALTER TABLE ${tablename} OWNER TO ${DATABASE_USER};"
                adjustTableNamesSql+="ALTER TABLE ${tablename} SET SCHEMA ${LEGACY_DATABASE_SCHEMA};"
                adjustTableNamesSql+="ALTER TABLE ${LEGACY_DATABASE_SCHEMA}.${tablename} RENAME TO ${tablename:6};"
	fi
done < <(psql --dbname postgresql://fmason:$password@127.0.0.1:5432/${DATABASE_NAME} -c "select tablename from pg_tables where schemaname = 'public';")

#adjust make the changes
psql --dbname postgresql://fmason:$password@127.0.0.1:5432/${DATABASE_NAME} --command "$adjustTableNamesSql"

#create the structure for the gwells tables
python ../../manage.py migrate

#replicate structure
#install crypto extension to support UUID creation
#replicate data
psql --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME}<<EOF
SELECT public.gwells_setup_replicate();
DROP EXTENSION IF EXISTS pgcrypto; CREATE EXTENSION pgcrypto;
SELECT public.gwells_replicate();
EOF
