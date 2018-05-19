FROM registry.access.redhat.com/rhscl/python-35-rhel7:3.5-24

USER 0

COPY contrib/ /tmp/contrib/
RUN source scl_source enable rh-python35 rh-nodejs6 && \
source ${APP_ROOT}/bin/activate && \
set -x && \
pip install -U pip setuptools wheel && \
pip install -r /tmp/contrib/requirements.txt && \
( cd /tmp/contrib &&  npm set progress=false && mkdir node_modules && npm install --no-bin-link ||  npm install --no-bin-link && tar zcf ${APP_ROOT}/npm-packages.tar.gz -C /tmp/contrib/node_modules/ .) && \
chown -R 1001:0 /opt/app-root && chmod -R og+rwx /opt/app-root && \
rm -rf /tmp/contrib

USER 1001
