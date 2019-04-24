FROM alpine:latest
USER root
RUN apk add --update \
    curl rsync \
    && rm -rf /var/cache/apk/*

# install restic
RUN curl -Lo restic.bz2 https://github.com/restic/restic/releases/download/v0.9.4/restic_0.9.4_linux_amd64.bz2 \
    && bzip2 -d restic.bz2 \
    && mv restic /usr/bin/restic \
    && chmod +x /usr/bin/restic 

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
USER 1001
