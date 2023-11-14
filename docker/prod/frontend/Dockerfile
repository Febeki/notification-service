FROM node:20-alpine

ENV APP_HOME=/frontend

WORKDIR $APP_HOME

RUN apk update

COPY ./frontend/*.json .
COPY ./frontend/*.js .

RUN npm ci --no-audit --no-fund --loglevel=error

COPY ./frontend/public ./public
COPY ./frontend/src ./src