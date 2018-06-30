FROM node:alpine as vuebuilder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ /app/frontend/
RUN ls
RUN npm run build

FROM python:3.5
WORKDIR /app/frontend
COPY --from=vuebuilder /app/frontend/webpack-stats.json .
WORKDIR /app/gwells/static/vue/
COPY --from=vuebuilder /app/frontend/dist/ ./
RUN pip install -U pip setuptools wheel

