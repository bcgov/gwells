FROM python:3.6

# Environment variables
#
ENV TERM xterm
ENV DEBIAN_FRONTEND noninteractive

# Packages and cleanup
#
RUN apt-get update; \
    apt-get install -y \
        binutils \
        gdal-bin \
        libgeoip-dev \
        libgeoip1 \
        libproj-dev \
        libspatialite-dbg \
        postgis \
        python-gdal; \
    apt-get autoclean; \
    apt-get clean; \
    rm -rf \
      /var/tmp/* \
      /var/lib/apt/lists/* \
      /tmp/* \
      /usr/share/doc/ \
      /usr/share/doc-base/ \
      /usr/share/man/

USER 1001
