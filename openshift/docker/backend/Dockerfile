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
        libproj-dev \
        gdal-bin; \
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
