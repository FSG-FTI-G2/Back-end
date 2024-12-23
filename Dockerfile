FROM python:3.11.10-slim-bookworm

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install --only main

COPY . /app

EXPOSE 7860

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "7860", "--loop", "asyncio"]