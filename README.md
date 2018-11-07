## VIKOverFlow (Backend)

### start

    # pip install pipenv
    $ pipenv install
    $ CONFIG_FILE=./config pipenv run src/manage.py migrate
    $ CONFIG_FILE=./config pipenv run src/manage.py runserver

### start with Docker
1. Create `Dockerfile` and `docker-compose.yml` in project directory.

`Dockerfile`:
```
FROM python:3.6-alpine
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk add build-base jpeg-dev zlib-dev graphviz-dev
RUN pip install pipenv
RUN pipenv install --system --dev
```

`docker-compose.yml`:
```
version: '3'

services:
  backend:
    build: .
    environment:
      - CONFIG_FILE=/code/config.yaml
    command: python src/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
```

2. `docker-compose up`

#### Running commands in docker container
While container is running:
```
docker-compose exec backend <command>
```
Example: `docker-compose exec backend python src/manage.py createsuperuser`

### policies

1. > Your code shall be meet the flake8 rules.
2. > Please do not be tricky, you have to think of simple solutions.
