#!/bin/bash
if [ "$ENVIRONMENT" = "local" ]; then
  echo "Running in local environment" &&
  sleep 3 &&
  set -x &&
  cd /app/backend &&
  mkdir -p .pip &&
  curl -s -o get-pip.py https://bootstrap.pypa.io/pip/3.5/get-pip.py && python3 get-pip.py && 
  python3 -m pip install --upgrade pip &&
  python3 -m pip install ptvsd &&
  python3 -m pip install --cache-dir=.pip -r requirements.txt &&
  python3 manage.py migrate --noinput &&
  ./load_fixtures.sh all &&
  python3 manage.py createinitialrevisions &&
  python3 manage.py collectstatic --noinput &&
  python3 manage.py export --cleanup=1 --upload=1 &&
  python3 manage.py runserver 0.0.0.0:8000
elif [ "$ENVIRONMENT" = "test" ]; then
  echo "Running in test environment" &&
  sleep 3 &&
  set -x &&
  cd /app/backend &&
  mkdir -p .pip &&
  python3 -m pip install --upgrade pip &&
  python3 -m pip install ptvsd &&
  python3 -m pip install --cache-dir=.pip -r requirements.txt &&
  python3 manage.py collectstatic --noinput &&
  python3 manage.py runserver 0.0.0.0:8000
fi
