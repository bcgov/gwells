#!/bin/bash
# using the && runs the second command only if the first succeeded
#https://askubuntu.com/questions/334994/which-one-is-better-using-or-to-execute-multiple-commands-in-one-line

psql -h 127.0.0.1 --username ${DATABASE_USER} --quiet --dbname ${DATABASE_NAME} --command "select gwells_setup_replicate();" &&
psql -h 127.0.0.1 --dbname ${DATABASE_NAME} --command "select gwells_replicate();"
