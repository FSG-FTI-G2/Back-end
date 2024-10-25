FROM python:3.10-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir celery[redis] kafka-python transformers torch

COPY . .

CMD ["celery", "-A", "app.app", "worker", "--loglevel=info"]