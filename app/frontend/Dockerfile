FROM node:22.12.0 as build

WORKDIR /app/frontend

COPY package*.json /app/frontend/

COPY . .

RUN set -x
RUN cd /app/frontend
RUN npm install

EXPOSE 8080
CMD ["npm", "run", "serve"]
