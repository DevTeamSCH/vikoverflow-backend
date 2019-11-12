FROM python:3.6-alpine

ENV CONFIG_FILE=/code/config.yaml
ENV PIP_NO_CACHE_DIR=false

RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev zlib-dev jpeg-dev &&\
    pip install --no-cache-dir pipenv psycopg2 typed-ast Pillow &&\
    apk del --no-cache .build-deps &&\
    apk add libpq zlib-dev jpeg-dev

RUN mkdir /code
WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev
# RUN pipenv install

COPY config.yaml ./
COPY src /code/

ENTRYPOINT ["./docker-entrypoint.sh"]
