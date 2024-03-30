# awsome-backend

- To remove git

```git
rm -rf .git*
```

- macos
  brew install pyenv
  pyenv install --list
  pyenv instal VERSION
  pyenv global VERSION

poetry init

poetry install

poetry shell

```cmd
pre-commit install
pre-commit run --all-files
```

Then create `.env` file (or rename and modify `.env.example`) in project root and set environment variables for application: ::

    touch .env
    echo APP_ENV=dev >> .env
    echo DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB >> .env
    echo SECRET_KEY=$(openssl rand -hex 32) >> .env

pytest --cov=tests --cov-fail-under=70

DOCKER_BUILDKIT=1 docker build -t ems-local .
docker run -e APP_ENV=dev -p 8000:8000 ems-local
