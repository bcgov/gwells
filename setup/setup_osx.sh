#!/bin/bash
#
set -eu


# Verbose option
#
[ ! -z "${VERBOSE+x}" ]&&[ "${VERBOSE}" == true ]&& \
	set -x


# Ensure bash shell script exists and store its checksum
#
BASHSS=~/.bash_profile
touch "${BASHSS}"
BASHSS_CHECKSUM=$( md5 -q "${BASHSS}" )


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
[ "$( git config --global --get user.email )" ] && \
	[ "( git config --global --get user.name)" ] || \
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
PACKAGES="git postgresql python3"
for p in $PACKAGES
do
	brew list $p || brew install $p
done


# Start PostgreSQL
#
( pg_isready -q )|| \
        brew services start postgresql


# Create postgres user
#
PSQLV=$( psql --version | sed 's/[^0-9\.]*//g' )
CUSER=$( find /usr/local/Cellar/postgresql -name createuser | grep "$PSQLV" )
psql -U postgres -c \
	"select 1 from pg_roles where rolname='postgres';" | grep '1' || \
	"${CUSER}" -s postgres


# Create db user and database
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


# Config bash shell to source virtualenvwrapper.sh
#
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
source "${BASHSS}"
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
export LEGACY_DATABASE_USER=wells
export LEGACY_DATABASE_NAME=wells
export LEGACY_SCHEMA=wells


# Pip3 install requirements
#
pip3 install -U -r ../requirements.txt


# Create dev database
#
python3 ../manage.py migrate


# Open browser window after delay
#
( sleep 3 && open http://127.0.0.1:8000/gwells ) &


# Run server
#
python3 ../manage.py runserver


# Recommend sourcing ~/.bash_profile if the file has changed
#
if [ "${BASHSS_CHECKSUM}" != $( md5 -q "${BASHSS}" ) ]
then
	echo
	echo "Warning: ~/.bash_profile has changed!  To source it type:"
	echo
	echo "source ~/.bash_profile "
fi
echo
