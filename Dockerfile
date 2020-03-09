FROM python:3.6.10-stretch

RUN pip install poetry

COPY pyproject.toml /app/
COPY poetry.lock /app/
WORKDIR /app
RUN poetry install --no-dev

COPY . /app
