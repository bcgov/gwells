#!/bin/bash
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

#collect authentication credentials for process

#get name of Superuser who will run the replication
# -p is for prompt
read -p "Superuser that will run the replication: " superuser &&

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
\include clear-tables.sql
\include create-xform-gwells-well-ETL-table.sql
\include copy-remote-code-tables.sql
\include populate-xform-gwells-well.sql
\include populate-gwells-from-xform.sql
\include setup-replicate.sql
\include replicate.sql
EOF

#restore the legacy data - superuser necessary because of ownership issues
pg_restore --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME} --no-owner $wellsdump &&

#create ${LEGACY_DATABASE_SCHEMA}
psql --dbname postgresql://${DATABASE_USER}:$password@127.0.0.1:5432/${DATABASE_NAME} <<EOF
CREATE SCHEMA ${LEGACY_DATABASE_SCHEMA};
EOF

#clean up permissions just in case
psql --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME} <<EOF
REVOKE ALL ON SCHEMA public FROM ${DATABASE_USER};
GRANT ALL ON SCHEMA public TO ${DATABASE_USER};
EOF

adjustTableNamesSql=""
adjustTableSchemaSql=""

#build the sql so that you only need one connection
#don't use a pipe because that creates a subshell and you'll lose your variable value
#-t for tuples only --- gets rid of header and footer
#-sed trims empty last line
while read -r tablename; do
	adjustTableNamesSql+="ALTER TABLE ${tablename} OWNER TO ${DATABASE_USER};"
	adjustTableSchemaSql+="ALTER TABLE ${tablename} SET SCHEMA ${LEGACY_DATABASE_SCHEMA};"
done < <(psql --dbname postgresql://fmason:$password@127.0.0.1:5432/${DATABASE_NAME} -t -c "select tablename from pg_tables where schemaname = 'public';" | sed -e '$d' )

#make the changes
psql --dbname postgresql://fmason:$password@127.0.0.1:5432/${DATABASE_NAME} --command "$adjustTableNamesSql"
psql --dbname postgresql://fmason:$password@127.0.0.1:5432/${DATABASE_NAME} --command "$adjustTableSchemaSql"

#create the structure for the gwells tables
python ../../manage.py makemigrations
python ../../manage.py migrate

#replicate structure
#install crypto extension to support UUID creation
#replicate data
psql --dbname postgresql://$superuser:$superuser_password@127.0.0.1:5432/${DATABASE_NAME}<<EOF
SELECT public.setup_replicate();
DROP EXTENSION IF EXISTS pgcrypto; CREATE EXTENSION pgcrypto;
SELECT public.replicate();
EOF
