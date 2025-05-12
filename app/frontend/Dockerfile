FROM node:22.12.0 as build

WORKDIR /app/frontend

COPY package*.json /app/frontend/

COPY . .

RUN set -x
RUN cd /app/frontend
RUN npm install
RUN npm install -g serve
RUN npm run build

FROM caddy:builder-alpine AS builder
RUN xcaddy build \
  --with github.com/caddyserver/replace-response
 
FROM caddy:2.8.4-alpine
COPY --from=builder /usr/bin/caddy /usr/bin/caddy

RUN apk add --no-cache ca-certificates

# Copy static files, verify Caddyfile formatting
COPY --from=build /app/frontend/dist /srv
COPY Caddyfile /etc/caddy/Caddyfile
RUN caddy fmt /etc/caddy/Caddyfile --overwrite

# Fix permissions for OpenShift
RUN chmod -R g+rwx /srv /etc/caddy /usr/bin/caddy \
    && chgrp -R 0 /srv /etc/caddy /usr/bin/caddy

# Boilerplate, not used in OpenShift/Kubernetes
EXPOSE 8080 3001

USER 1001
