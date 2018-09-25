FROM node:8
RUN mkdir /webapp
WORKDIR /app/frontend
ADD frontend/package.json .
RUN npm install
ADD . /app/
RUN npm rebuild node-sass
