FROM node:20-alpine

WORKDIR /usr/src/frontend

COPY ./frontend/*.json .

RUN npm install

COPY ./frontend/public ./public
COPY ./frontend/src ./src