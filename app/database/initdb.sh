#!/bin/bash
echo "Adding tile server user"
psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "CREATE USER ftw_reader WITH PASSWORD '${POSTGRES_PASSWORD}';"