FROM openshift/bcgov-s2i-caddy:latest
USER 0
COPY staticfiles /var/www/html/gwells/static
RUN ls -la /var/www/html/gwells/static/
USER 1001
CMD [\"sh\",\"/tmp/scripts/run\"]
