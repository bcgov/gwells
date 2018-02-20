#!/bin/bash
#
set -eux


# Install Homebrew
#
which brew || \
	/usr/bin/ruby -e "$( curl -fsSL \
	https://raw.githubusercontent.com/Homebrew/install/master/install )"


# Brew install packages
#
PACKAGES="git python3"
for p in $PACKAGES
do
	which $p || brew install $p
done


# Configure git
#
git config --global --get push.default || \
	git config --global push.default simple
git config --global --get user.email && \
	git config --global --get user.name || \
	git config --global --edit


# PostgreSQL - install, enable service and initialize db
#
if( ! which psql );
then
	brew install postgresql
	brew services start postgresql
	initdb /usr/local/var/postgres/
fi


# Create postgres user
#
PSQLV=$( psql --version | sed 's/[^0-9\.]*//g' )
CUSER=$( find /usr/local/Cellar/postgresql -name createuser | grep "$PSQLV" )
psql -U postgres -c "select 1 from pg_roles where rolname='postgres';" || \
	"${CUSER}" -s postgres


# Create user and database
#
psql -U postgres -c "SELECT 1 FROM pg_roles WHERE rolname='gwells';" || \
	psql -U postgres -c "CREATE USER gwells WITH createdb;"
psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname='gwells';" || \
	psql -U postgres -c "CREATE DATABASE gwells WITH OWNER='gwells';"


# Pip3 install virtualenv and virtualenvwrapper
#
PACKAGES="virtualenv virtualenvwrapper"
for p in $PACKAGES
do
	pip3 show $p || echo pip3 install --user $p
done
