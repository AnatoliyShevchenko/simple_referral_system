FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY scripts /scripts

RUN chmod +x /scripts/wait-for.sh /scripts/entrypoint.sh