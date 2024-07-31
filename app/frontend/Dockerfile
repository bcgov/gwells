FROM node:18.12.0-slim

# RUN apt-get -y update

# RUN apt-get -y install git build-essential

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    make \
    g++

WORKDIR /app

COPY package*.json ./

RUN npm install --legacy-peer-deps 

COPY . /app

RUN npm i --legacy-peer-deps && npm run build --legacy-peer-deps