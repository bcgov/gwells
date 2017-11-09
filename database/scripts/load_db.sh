#!/bin/bash -x
# Add -x beside  #!/bin/bash to debug. It will print out the executed commands.

# to make conventient use of this script in ##development## edit your pg_hba.conf file to set users to be trusted locally
# https://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html

# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

python ../../manage.py makemigrations &&
python ../../manage.py migrate &&

cd ../code-tables &&

#copy code tables
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
\include clear-tables.sql
\include data-load-static-codes.sql
EOF

cd ../scripts

#replicate
psql --dbname postgresql://${DATABASE_USER}:${DATABASE_USER_PASSWORD}@127.0.0.1:5432/${DATABASE_NAME} <<EOF
\include create-xform-gwells-well-ETL-table.sql
\include populate-xform-gwells-well.sql
\include populate-gwells-well-from-xform.sql
\include migrate_screens.sql
EOF
