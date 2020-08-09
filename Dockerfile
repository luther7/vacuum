FROM python:3.8 AS base

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry && poetry config virtualenvs.create false

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["--help"]

COPY poetry.lock pyproject.toml /app/


FROM base AS dev

RUN poetry install --no-interaction --no-root

COPY . ./

RUN poetry install --no-interaction


FROM base AS prod

COPY . ./

RUN poetry install --no-interaction --no-dev
