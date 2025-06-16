FROM python:3.12.11-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./

RUN python -m pip install --upgrade --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root --without dev\
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY ./ ./