FROM python:3.14.8-trixie@sha256:a11116e648ddd8a05e1120014c8e6ac259f718040b67e2dcd6a7c0b7bab3ff2c AS base

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --no-cache-dir pip-tools

COPY pyproject.toml .

RUN pip-compile pyproject.toml --output-file=- | pip install --no-cache-dir -r /dev/stdin


FROM base AS dev


FROM base AS prod

COPY app ./app
COPY services/alembic ./services/alembic
COPY main.py .
