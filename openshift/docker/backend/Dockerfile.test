# TODO: we need to bump python version up once we get Django bumped up
FROM python:3.6-slim

RUN apt-get -y update

# RUN apt-get -y install git build-essential libgdal-dev -> maybe this is overkill?
RUN apt-get -y install git build-essential libgdal-dev 

ENV PATH="/usr/bin/python3:${PATH}"

WORKDIR /app

# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

RUN python3 -m pip install 'setuptools<58.0'
RUN python3 -m pip install --upgrade pip

COPY . /app

# RUN pwd

# RUN chmod +x load_fixtures.sh works when i pull the dockerfile into backend but not when dockerfile is with other docker files
RUN chmod +x /app
