# FROM python:3.7

# WORKDIR /app/backend

# # whitebox_tools is added to the context dir by the BuildConfig, which
# # copies it from the whiteboxtools:latest imagestream.
# # the BuildConfig also copies whitebox_tools.py (WBT Python bindings)
# # into the context dir so it gets copied by the COPY directive below.
# # COPY /wbt/target/x86_64-unknown-linux-musl/release/whitebox_tools /usr/local/bin/
# # COPY /wbt/whitebox_tools.py /app/

# # RUN useradd wally -M -G root -u 1021 && chmod -R 775 /app \
# #   && chown -R wally:root /app \ 
# #   && apt-get update && apt-get -y install ca-certificates libgdal-dev gdal-bin

# COPY ./requirements.txt /

# RUN pip install -r /requirements.txt

# COPY . /app/backend

# ENV PYTHONPATH=/app/backend
# # RUN pytest /app/tests/ -W ignore::DeprecationWarning

# EXPOSE 8000

# # Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# # And then will start Gunicorn with Uvicorn
# CMD ["/app/backend/start.sh"]

FROM artifacts.developer.gov.bc.ca/g26e-backend-docker-local/gwells-backend:1.0 AS base

FROM base
WORKDIR /app

COPY . .
