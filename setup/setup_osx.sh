#!/bin/bash


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Receive a GWells and Wells (legacy) databases to import
#
DB_MODERN=${DB_MODERN:-''}
DB_LEGACY=${DB_LEGACY:-''}


# Post deploy and test options
#
POST_DEPLOY=${POST_DEPLOY:-false}
TEST=${TEST:-false}


# GWells environment variables
#
DATABASE_SERVICE_NAME="${DATABASE_SERVICE_NAME:-postgresql}"
DATABASE_ENGINE="${DATABASE_ENGINE:-postgresql}"
DATABASE_NAME="${DATABASE_NAME:-gwells}"
DATABASE_USER="${DATABASE_USER:-gwells}"
DATABASE_PASSWORD="${DATABASE_PASSWORD:-gwells}"
DATABASE_SCHEMA="${DATABASE_SCHEMA:-public}"
DJANGO_DEBUG="${DJANGO_DEBUG:-True}"
APP_CONTEXT_ROOT="${APP_CONTEXT_ROOT:-gwells}"
ENABLE_GOOGLE_ANALYTICS="${ENABLE_GOOGLE_ANALYTICS:-False}"
ENABLE_DATA_ENTRY="${ENABLE_DATA_ENTRY:-True}"
BASEURL="${BASEURL:-http://gwells-dev.pathfinder.gov.bc.ca/}"
LEGACY_DATABASE_USER="${LEGACY_DATABASE_USER:-wells}"
LEGACY_DATABASE_NAME="${LEGACY_DATABASE_NAME:-wells}"
LEGACY_SCHEMA="${LEGACY_SCHEMA:-wells}"
LEGACY_DATABASE_PW="${LEGACY_DATABASE_PW:-wells}"          # For Wells db import
DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-'9e4@&tw46\$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'}"
SESSION_COOKIE_SECURE="${SESSION_COOKIE_SECURE:-False}"
CSRF_COOKIE_SECURE="${CSRF_COOKIE_SECURE:-False}"
ENABLE_ADDITIONAL_DOCUMENTS="${ENABLE_ADDITIONAL_DOCUMENTSL:-False}"
DJANGO_ADMIN_URL="${DJANGO_ADMIN_URL:-admin}"


# Check for params, output a message
#
if([ "$#" -ne 0 ])
then
	set +x
	echo
	echo "Please use variables to pass this script commands."
	echo "E.g.:"
	echo " 'VERBOSE=true ./setup_osx.sh'"
	echo " 'DB_MODERN=<path>/<filename>.dmp DB_LEGACY=<path>/<filename>.dmp ./setup_osx.sh'"
	echo " 'TEST=true ./setup_osx.sh'"
	echo
	exit
fi


# Ensure bash shell script exists and store its checksum
#
BASH_SS=${BASH_SS:-~/.bash_profile}
touch "${BASH_SS}"
BASHSS_CHECKSUM=$( md5 -q "${BASH_SS}" )


# Save start directory
#
START_DIR=$( pwd )


# Install Xcode command line tools
#
while ( xcode-select --install );
do
	xcode-select --install
	echo "Waiting for Xcode Developer Tools Install"
	sleep 30
done


# Request and wait for Java 8 install
#
( which java )&&( /usr/libexec/java_home -x | grep -o "1.8" )||( \
	tput bel
	echo
	echo "Warning: to perform gradlew tests Oracle Java 8 is required!"
	echo
	read -n 1 -p "Open download link and wait for install? (y|n):" yORn
	echo
	if([ "${yORn}" == "y" ]||[ "${yORn}" == "Y" ])
	then
		open http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

		while ! (( which java )&&( /usr/libexec/java_home -x | grep -o "1.8" ))
		do
			echo "Waiting for Java 8 Install"
			sleep 30
		done
	fi
)


# Configure git and set remote (upstream) origin
#
[ "$( git config --global --get push.default )" == "simple" ] || \
	git config --global push.default simple
[ "$( git config --global --get core.autocrlf)" == "input" ] || \
	git config --global core.autocrlf input
[ "$( git config --global --get user.email )" ]&&[ "( git config --global --get user.name)" ] || \
	git config --global --edit
#
git remote -v | grep "bcgov/gwells.git (push)" || \
	git remote add upstream https://github.com/bcgov/gwells.git


# Install Homebrew
#
which brew || \
	/usr/bin/ruby -e "$( curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install )"


# Brew install packages
#
PACKAGES=(
	"git"
	"nodejs"
	"postgresql"
	"python3"
)
for p in ${PACKAGES[@]}
do
	brew list $p || brew install $p
done


# Start PostgreSQL
#
if( ! pg_isready -q )
then
	brew services start postgresql
	sleep 3
fi


# Create postgres user
#
PSQLV=$( psql --version | sed 's/[^0-9\.]*//g' )
CUSER=$( find /usr/local/Cellar/postgresql -name createuser | grep "$PSQLV" )
psql -U postgres -c \
	"select 1 from pg_roles where rolname='postgres';" | grep '1' || \
	"${CUSER}" -s postgres


# Create GWells and Wells (legacy) postgres user and database
#
COMMANDS=(
	"DROP DATABASE IF EXISTS gwells;"
	"DROP USER IF EXISTS gwells;"
	"CREATE USER gwells WITH createdb;"
	"ALTER USER gwells WITH PASSWORD 'gwells';"
	"CREATE DATABASE gwells WITH owner='gwells';"
	"DROP DATABASE IF EXISTS wells;"
	"DROP USER IF EXISTS wells;"
	"CREATE USER wells;"
	"ALTER USER wells WITH PASSWORD 'wells';"
	"CREATE DATABASE wells WITH owner='wells';"
)
for c in ${COMMANDS[@]}
do
	psql -U postgres -c $c
done


# Prepare GWells for foreign data wrapper
#
COMMANDS=(
	"CREATE EXTENSION IF NOT EXISTS pgcrypto;"
	"CREATE EXTENSION IF NOT EXISTS postgres_fdw;"
)
for c in ${COMMANDS[@]}
do
	psql -U postgres -d gwells -c $c
done


# Restore the legacy database from a database dump
#
[ -z ${DB_LEGACY} ]|| \
	pg_restore -U wells -d wells --no-owner --no-privileges "${DB_LEGACY}"


# Create foreign data wrapper linking Wells (legacy) to the GWells database
#
COMMANDS=(
	"DROP SERVER IF EXISTS wells CASCADE;"
	"CREATE SERVER wells FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'localhost', dbname 'wells');"
	"DROP USER MAPPING IF EXISTS FOR public SERVER wells;"
	"CREATE USER MAPPING FOR PUBLIC SERVER wells OPTIONS (user 'wells', password 'wells');"
	"CREATE SCHEMA IF NOT EXISTS wells;"
	"IMPORT FOREIGN SCHEMA public FROM SERVER wells INTO wells;"
	"GRANT usage ON SCHEMA wells TO gwells;"
	"GRANT select ON ALL TABLES in SCHEMA wells TO wells;"
	"CREATE SCHEMA IF NOT EXISTS wells;"
)
for c in ${COMMANDS[@]}
do
	psql -U postgres -d gwells -c $c
done


# Pip3 install virtualenv and virtualenvwrapper
#
pip3 install --upgrade pip
PACKAGES="
	virtualenv
	virtualenvwrapper
"
for p in $PACKAGES
do
	pip3 show $p || pip3 install $p --user
done


# Config bash shell to source virtualenvwrapper.sh
#
VEWSRC=$( find ~ -name virtualenvwrapper.sh | grep -m 1 . )
grep --quiet "virtualenvwrapper.sh" "${BASH_SS}" || \
	(
		echo ;
		echo "# Setup mkvirtualenv";
		echo "#";
		echo "PATH=${PATH}:~/Library/Python/3.6/bin";
		echo "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3";
		echo "source ${VEWSRC}"
	) >> "${BASH_SS}"


# Set JAVA_HOME to use version 8
#
grep --quiet "export JAVA_HOME=" ~/.bash_profile || \
	(
		echo ;
		echo "# Set Java 8 as default";
		echo "#";
		echo "export JAVA_HOME=$( /usr/libexec/java_home -v 1.8 )";
	) >> ~/.bash_profile


# Make virtual environment
#
PATH="${PATH}":~/Library/Python/3.6/bin
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
set +u
source "${BASH_SS}"
mkvirtualenv gwells || true
workon gwells
set -u


# Create and populate a postacticate file (like .bashrc for virtualenv)
#
ENV_VARS=(
	"export DATABASE_SERVICE_NAME=${DATABASE_SERVICE_NAME}"
	"export DATABASE_ENGINE=${DATABASE_ENGINE}"
	"export DATABASE_NAME=${DATABASE_NAME}"
	"export DATABASE_USER=${DATABASE_USER}"
	"export DATABASE_PASSWORD=${DATABASE_PASSWORD}"
	"export DATABASE_SCHEMA=${DATABASE_SCHEMA}"
	"export DJANGO_DEBUG=${DJANGO_DEBUG}"
	"export APP_CONTEXT_ROOT=${APP_CONTEXT_ROOT}"
	"export ENABLE_GOOGLE_ANALYTICS=${ENABLE_GOOGLE_ANALYTICS}"
	"export ENABLE_DATA_ENTRY=${ENABLE_DATA_ENTRY}"
	"export BASEURL=${BASEURL}"
	"export LEGACY_DATABASE_USER=${LEGACY_DATABASE_USER}"
	"export LEGACY_DATABASE_NAME=${LEGACY_DATABASE_NAME}"
	"export LEGACY_SCHEMA=${LEGACY_SCHEMA}"
	"export DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}"
	"export SESSION_COOKIE_SECURE=${SESSION_COOKIE_SECURE}"
	"export CSRF_COOKIE_SECURE=${CSRF_COOKIE_SECURE}"
	"export ENABLE_ADDITIONAL_DOCUMENTS=${ENABLE_ADDITIONAL_DOCUMENTS}"
	"export DJANGO_ADMIN_URL=${DJANGO_ADMIN_URL}"
)
#
PA_FILE=~/.virtualenvs/gwells/bin/postactivate
if [ ! -f "${PA_FILE}" ]
then 	(
		echo "#!/bin/bash"
		echo "#"
		for e in ${ENV_VARS[@]}
		do
			echo $e
		done
	) > "${PA_FILE}"
fi


# Install requirements with PIP3 and NPM
#
cd "${START_DIR}"/..
pip3 install -U -r requirements.txt
cd "${START_DIR}"/../frontend
npm install
npm run build


# Dev only - adapt schema for GWells
#
cd "${START_DIR}"/..
python3 manage.py makemigrations


# Migrate data from Wells (legacy) to GWells schema
#
python3 manage.py migrate


# Restore the GWells (modern) database from a dump
#
[ -z ${DB_MODERN} ]|| \
	pg_restore -U gwells -d gwells --no-owner --no-privileges "${DB_MODERN}"


# Collect static files and run tests
#
if [ "${TEST}" == "true" ]
then
	python3 manage.py collectstatic
	python3 manage.py test -c nose.cfg
fi


# Link to resemble OpenShift's /app-root/src directory
#
SOURCE_DIR=$( cd "${START_DIR}/.."; pwd )
TARGET_DIR=/opt/app-root
TARGET_LNK="${TARGET_DIR}/src"
[ -d "${TARGET_DIR}" ]|| sudo mkdir -p "${TARGET_DIR}"
if(
	[ -L "${TARGET_LNK}" ]&& \
	[ $( readlink -- "${TARGET_LNK}" ) != "${SOURCE_DIR}" ]
)
then
	sudo unlink "${TARGET_LNK}"
fi
[ -L "${TARGET_LNK}" ]|| \
	sudo ln -s "${SOURCE_DIR}" "${TARGET_LNK}"


# Post deploy
#
if [ "${POST_DEPLOY}" == "true" ]
then
	cd "${START_DIR}"/../openshift/scripts/
	./post-deploy.sh
fi


# Open browser window after delay
#
( sleep 3 && open http://127.0.0.1:8000/gwells ) &


# Run server
#
cd "${START_DIR}"
python3 ../manage.py runserver || true


# Recommend sourcing ~/.bash_profile if the file has changed
#
if [ "${BASHSS_CHECKSUM}" != $( md5 -q "${BASH_SS}" ) ]
then
	echo
	echo "Warning: ~/.bash_profile has changed!  To source it type:"
	echo
	echo "source ~/.bash_profile "
fi
echo
