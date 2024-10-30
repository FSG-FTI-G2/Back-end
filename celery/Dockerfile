FROM python:3.10-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir celery[redis,gevent]

# Install tasks dependencies
# If is there any other dependencies, add them as new lines
RUN pip install --no-cache-dir sentence-transformers

COPY . /app

CMD ["celery", "--app", "main", "worker", "--loglevel=INFO"]