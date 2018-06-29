FROM openshift/nodejs:8 as vuebuilder
WORKDIR /app
COPY /opt/app-root/src/gwells/app/package*.json .
RUN npm install
COPY /opt/app-root/src/gwells/frontend/* .
RUN npm run build

FROM openshift/python:3.5
WORKDIR ${APP_ROOT}/frontend
COPY --from=vuebuilder /app/webpack-stats.json .
COPY --from=vuebuilder /app/dist /op/app-root/src/gwells/static/vue
RUN source scl_source enable rh-python35 && \
source ${APP_ROOT}/bin/activate && \
pip install -U pip setuptools wheel
