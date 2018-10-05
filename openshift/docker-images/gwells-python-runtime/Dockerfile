FROM openshift/python:3.6
WORKDIR /packages
ADD . ../../../app/frontend/package.json
ADD . app/backend/requirements.txt
RUN source scl_source enable rh-python36 && \
source ${APP_ROOT}/bin/activate && \
pip install -U pip setuptools wheel && \
ls && ls / && ls /packages && pip install -r requirements.txt && \
cd /packages && npm install
