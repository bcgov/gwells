FROM node:8-alpine
RUN mkdir /webapp
WORKDIR /webapp
ADD package.json /webapp/
RUN npm install
ADD . /webapp/
RUN npm rebuild node-sass

