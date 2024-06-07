FROM python:3.7-slim

RUN apt-get -y update

RUN apt-get -y install git build-essential libgdal-dev 

ENV PATH="/usr/bin/python3:${PATH}"

WORKDIR /app

RUN python3 -m pip install 'setuptools<58.0'
RUN python3 -m pip install --upgrade pip

COPY . /app

# RUN chmod +x load_fixtures.sh works when i pull the dockerfile into backend but not when dockerfile is with other docker files
RUN chmod +x /app
