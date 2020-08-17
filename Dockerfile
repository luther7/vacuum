FROM python:3.8 AS base

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.10

RUN pip install poetry==$POETRY_VERSION \
  && poetry config virtualenvs.create false

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["grubbin", "webserver"]

COPY poetry.lock pyproject.toml /app/


FROM base AS dev

RUN poetry install --no-interaction --no-root

COPY . ./

RUN poetry install --no-interaction


FROM base AS prod

COPY . ./

RUN poetry install --no-interaction --no-dev
