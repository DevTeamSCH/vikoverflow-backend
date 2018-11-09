FROM python:3.6-alpine
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk add build-base jpeg-dev zlib-dev graphviz-dev postgresql-dev musl-dev gcc
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --dev
