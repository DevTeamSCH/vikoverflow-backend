FROM python:3.6-alpine
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk add build-base jpeg-dev zlib-dev graphviz-dev
RUN pip install pipenv
RUN pipenv install --system --dev
