#!/bin/bash
#
set -eux


# Install Homebrew
#
which brew || \
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


# Brew install packages
#
PACKAGES="git postgresql python3"
for p in $PACKAGES
do
	which $p || brew install $p
done


# Configure git
#
git config --global --get push.default ||
	git config --global push.default simple
git config --global --get user.email &&
	git config --global --get user.name ||
	git config --global --edit


# Enable postgres service (now + boot)
#
brew services start postgresql


# Initialize db
#
initdb /usr/local/var/postgres/


# Create user
#
PSQL_VER=$( psql --version | sed 's/[^0-9\.]*//g' )
CREATE_U=$( sudo find /usr/local/Cellar -name createuser | grep postgresql | grep "$PSQL_VER" )
"${CREATE_U}" -s postgres
