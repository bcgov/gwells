#!/bin/sh
# pre-deploy hook that runs migrations for GWELLS app.

set -xeuo pipefail

python manage.py migrate
