## VIKOverFlow (Backend)

### start

    # pip install pipenv
    $ pipenv install
    $ CONFIG_FILE=./config.yaml pipenv run src/manage.py migrate
    $ CONFIG_FILE=./config.yaml pipenv run src/manage.py runserver

### start with Docker

```
$ docker volume create --name vikoverflow-data
$ docker-compose up
```

#### running commands in docker container
```
$ docker-compose exec backend <command>
```
Example:
```
$ docker-compose exec backend python src/manage.py migrate
```

### policies

1. > Your code shall be meet the flake8 rules.
2. > Please do not be tricky, you have to think of simple solutions.
