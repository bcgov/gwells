FROM alpine:latest
USER root
RUN apk add --update \
    curl \
    && rm -rf /var/cache/apk/*

# install restic and rclone tools.
RUN curl -Lo restic.bz2 https://github.com/restic/restic/releases/download/v0.9.4/restic_0.9.4_linux_amd64.bz2 \
    && bzip2 -d restic.bz2 \
    && mv restic /usr/bin/restic \
    && chmod +x /usr/bin/restic \
    && curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip \
    && unzip rclone-current-linux-amd64.zip \
    && cd rclone-*-linux-amd64 \
    && cp rclone /usr/bin/ \
    && chown root:root /usr/bin/rclone \
    && chmod 755 /usr/bin/rclone

# copy rclone config.  rclone will look for a config file at /.rclone.conf
COPY ./rclone.conf /.rclone.conf
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
USER 1001
