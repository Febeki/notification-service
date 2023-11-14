FROM python:3.11-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/backend

RUN apk add --update --no-cache curl && \
    mkdir -p /gunicorn_socket /redis_socket && \
    chmod -R 777 /gunicorn_socket /redis_socket


WORKDIR $APP_HOME

COPY ./backend/backend/requirements/base.txt ./backend/backend/requirements/prod.txt ./
RUN pip install --upgrade pip
RUN pip install -r prod.txt

COPY ./docker/prod/backend/entrypoint.sh /
COPY ./backend .

RUN chmod +x /*.sh

ENTRYPOINT ["/entrypoint.sh"]