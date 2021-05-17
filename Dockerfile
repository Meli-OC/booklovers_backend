# Pull official image
FROM python:3.9.2-alpine3.12 as python-base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# Install system dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk update && apk add python3-dev \
        gcc libc-dev linux-headers postgresql-dev \
        libffi-dev openssl-dev cargo
RUN apk add musl-dev freetype libpng libjpeg-turbo freetype-dev libpng-dev libjpeg-turbo-dev

# Install python dependencies and packages
COPY poetry.lock pyproject.toml /app/
RUN pip install --no-cache --upgrade pip \
    && pip install --no-cache poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

