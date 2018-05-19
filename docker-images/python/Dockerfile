FROM openshift/python:3.5

COPY contrib/ /tmp/contrib/

RUN source scl_source enable rh-python35 && \
source ${APP_ROOT}/bin/activate && \
pip install -U pip setuptools wheel && \
pip install -r /tmp/contrib/requirements.txt && \
( cd /tmp/contrib &&  npm install && mv node_modules ${APP_ROOT}/)

