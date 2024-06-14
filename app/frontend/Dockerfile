FROM node:14.21.3-slim

# RUN apt-get -y update

# RUN apt-get -y install git build-essential

RUN apt-get update && apt-get install -y \
    python \
    make \
    g++

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . /app

RUN npm i && npm run build