#!/bin/bash
#
set -eu


# Verbose option
#
[ ! -z "${VERBOSE+x}" ]&&[ "${VERBOSE}" == true ]&& \
	set -x


# Install Xcode command line tools
#
while ( xcode-select --install );
	do xcode-select --install
	echo "Waiting for Xcode Developer Tools Install"
	sleep 60
done


# Configure git and set remote (upstream) origin
#
git config --global --get push.default || \
	git config --global push.default simple
git config --global --get user.email && \
	git config --global --get user.name || \
	git config --global --edit
#
git remote -v | grep "https://github.com/bcgov/gwells.git (push)" || \
	git remote add upstream https://github.com/bcgov/gwells.git


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
	brew list $p || brew install $p
done


# Brew install PostgreSQL
#
( which psql )|| \
        brew install postgresql


# Start PostgreSQL
#
( pg_isready -q )|| \
        brew services start postgresql


# Create postgres user
#
PSQLV=$( psql --version | sed 's/[^0-9\.]*//g' )
CUSER=$( find /usr/local/Cellar/postgresql -name createuser | grep "$PSQLV" )
psql -U postgres -c "select 1 from pg_roles where rolname='postgres';" || \
	"${CUSER}" -s postgres


# Create user and database
#
psql -U postgres -c \
	"SELECT 1 FROM pg_roles WHERE rolname='gwells';" | grep '1' || \
	psql -U postgres -c "CREATE USER gwells WITH createdb;"
psql -U postgres -c \
	"SELECT 1 FROM pg_database WHERE datname='gwells';" | grep '1' || \
	psql -U postgres -c "CREATE DATABASE gwells WITH OWNER='gwells';"


# Pip3 install virtualenv and virtualenvwrapper
#
PACKAGES="virtualenv virtualenvwrapper"
for p in $PACKAGES
do
	pip3 show $p || pip3 install $p --user
done


# Pip3 install requirements
#
pip3 install -U -r ../requirements.txt


# Config bash shell to source virtualenvwrapper.sh
#
BASHSS=~/.bash_profile
touch "${BASHSS}"
VEWSRC=$( find ~ -name virtualenvwrapper.sh | grep -m 1 . )
grep --quiet "virtualenvwrapper.sh" "${BASHSS}" || \
	(
		echo ;
		echo "# Setup mkvirtualenv";
		echo "#";
		echo "PATH=${PATH}:~/Library/Python/3.6/bin";
		echo "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3";
		echo "source ${VEWSRC}"
	) >> "${BASHSS}"


# Make virtual environment
#
PATH="${PATH}":~/Library/Python/3.6/bin
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
set +u
source "${VEWSRC}"
mkvirtualenv gwells || true
workon gwells
set -u


# Configure database with environment variables
#
export DATABASE_SERVICE_NAME=postgresql
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=gwells
export DATABASE_USER=gwells
export DATABASE_PASSWORD=gwells
export DATABASE_SCHEMA=public
export DJANGO_DEBUG=True
export APP_CONTEXT_ROOT=gwells
export ENABLE_GOOGLE_ANALYTICS=False
export ENABLE_DATA_ENTRY=True
export BASEURL=http://gwells-dev.pathfinder.gov.bc.ca/


# Create dev database
#
python3 ../manage.py migrate


# Open browser window after delay
#
( sleep 3 && open http://127.0.0.1:8000/gwells ) &


# Run server
#
python3 ../manage.py runserver
