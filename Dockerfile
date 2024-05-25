FROM python:3.10.14-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE 8000



FROM base as builder

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        tree \
        ssh \
        git \
        netcat-traditional \
    && rm -r /var/lib/apt/lists/*

ENV POETRY_HOME=/etc/poetry \
    POETRY_VERSION=1.1.12 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.3.2

# Copy wait-for script
COPY wait-for /usr/local/bin/wait-for
RUN chmod +x /usr/local/bin/wait-for


FROM builder as development

COPY usr_local /usr/local
COPY app /app/app
COPY config /app/config
COPY setup.cfg /root/.config/flake8

CMD uvicorn --reload --host=0.0.0.0 --port=8000 app.api:app



FROM builder as local-development

#RUN mkdir -m 700 /root/.ssh \
#    && touch -m 600 /root/.ssh/known_hosts \
#    && ssh-keyscan git.grtech.pl > /root/.ssh/known_hosts

COPY ./pyproject.toml ./poetry.lock ./
RUN --mount=type=ssh $POETRY_HOME/bin/poetry install --no-root

COPY app /app/app
COPY config /app/config
COPY setup.cfg /root/.config/flake8

CMD uvicorn --reload --host=0.0.0.0 --port=8000 app.api:app



FROM base as release

ENV ENABLE_METRICS=true \
    VERSION=1.0.0

COPY usr_local /usr/local
COPY app /app/app
COPY config /app/config

CMD uvicorn --host=0.0.0.0 --port=8000 --log-config config/logging.conf app.api:app --proxy-headers
