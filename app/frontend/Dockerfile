FROM node:22.12.0 as build

WORKDIR /app/frontend

COPY package*.json /app/frontend/

COPY . .

RUN set -x
RUN cd /app/frontend
RUN npm ci
RUN npm install -g serve
RUN npm run build

# Final image
FROM caddy:2.7.6-alpine

RUN apk add --no-cache ca-certificates

# Copy static files, verify Caddyfile formatting
COPY --from=build /app/frontend/dist /srv
COPY ./Caddyfile /etc/caddy/Caddyfile
RUN caddy fmt /etc/caddy/Caddyfile --overwrite

# Copy env.js separately to make sure it's in the right place
COPY ./public/env.js /srv/env.js

# Fix permissions
RUN chmod -R g+rwx /srv /etc/caddy /usr/bin/caddy /config/caddy \
    && chgrp -R 0 /srv /etc/caddy /usr/bin/caddy /config/caddy

# Boilerplate, not used in OpenShift/Kubernetes
EXPOSE 8080 3001

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile" ]
USER 1001

