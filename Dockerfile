FROM python:3.6-alpine

ENV CONFIG_FILE=/code/config.yaml

RUN mkdir /code
ADD . /code
WORKDIR /code

RUN apk add build-base jpeg-dev zlib-dev graphviz-dev postgresql-dev musl-dev gcc && \
    pip install pipenv && \
    pipenv lock && \
    pipenv install --system --dev

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
