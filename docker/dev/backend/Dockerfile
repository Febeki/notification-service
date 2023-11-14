FROM python:3.11-alpine3.15

WORKDIR /usr/src/backend


COPY ./backend/backend/requirements/base.txt ./backend/backend/requirements/dev.txt ./
RUN pip install -r dev.txt

COPY ./docker/dev/backend/entrypoint.sh /
COPY ./backend .

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]