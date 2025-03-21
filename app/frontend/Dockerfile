FROM node:22.12.0 as build

WORKDIR /app/frontend

COPY package*.json /app/frontend/

COPY . .

RUN set -x
RUN cd /app/frontend
RUN npm install
RUN npm run build
RUN npm install -g serve

EXPOSE 8080
CMD ["serve", "-s", "dist", "-l", "8080"]

# RUN set -x
# RUN cd /app/frontend
# RUN npm install
# RUN npm run build

# EXPOSE 8080
# CMD ["npm", "run", "serve"]

# We got to the point where the frontend is completely separate from the backend build and deploy and it runs locally. However, we need to fix the vite build

# Do some reading on setting up a vite vue project
# Create backend dockerfile with docker compose pointing
# Create new branch and try to get frontend to run locally