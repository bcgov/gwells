FROM python:3.7

# Install dependencies
RUN apt -y update && apt -y install git build-essential gdal-bin libgdal-dev postgresql-client

ENV PATH="/usr/bin/python3:${PATH}"

WORKDIR /app/backend

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install ptvsd
RUN python3 -m pip install 'setuptools<58.0'

COPY . /app/backend

# RUN chmod +x load_fixtures.sh works when i pull the dockerfile into backend but not when dockerfile is with other docker files
RUN chmod -R +x /app/backend
# RUN chmod -R 777 /app 
# RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install -r requirements.txt

# TODO: move to entrypoint in deployment template?
# chmod -R 777 /app && \
# CMD [""]

CMD sh -c "python3 manage.py migrate --noinput && \
    ./load_fixtures.sh all && \
    python3 manage.py createinitialrevisions && \
    python3 manage.py collectstatic --noinput && \
    # python3 manage.py export --cleanup=1 --upload=1 && \
    python3 manage.py runserver 0.0.0.0:8000"

USER 1001
