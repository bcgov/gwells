FROM openshift/nodejs:8 AS builder
WORKDIR /app/frontend
COPY ${APP_ROOT}/src/gwells/app/package*.json ./
RUN npm install
COPY ${APP_ROOT}/src/gwells/frontend/ /app/frontend/
RUN npm run build

FROM openshift/python:3.5
WORKDIR ${APP_ROOT}/frontend
COPY --from=builder /app/frontend/webpack-stats.json .
COPY --from=builder /app/frontend/dist/ ${APP_ROOT}/src/gwells/static/vue/
RUN source scl_source enable rh-python35 && \
source ${APP_ROOT}/bin/activate && \
pip install -U pip setuptools wheel
