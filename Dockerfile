FROM python:3.6-alpine

ENV CONFIG_FILE=/code/config.yaml
ENV PIP_NO_CACHE_DIR=false


RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock ./

RUN apk add --no-cache --virtual .deps build-base jpeg-dev zlib-dev graphviz-dev musl-dev gcc postgresql-dev && \
    pip install pipenv && \
    pipenv install --system --dev && \
    apk del --no-cache .deps && \
    apk add --no-cache libpq libjpeg zlib

COPY config.yaml ./
COPY ./src ./src

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
