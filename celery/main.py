import os
from celery import Celery
from tasks.echo import echo
from tasks.embedding import embed_model

CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', 6379)}/0"

app = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)


@app.task(name="echo", bind=True)
def echo_task(self, input_data: str):
    """ Test Celery Task """
    return echo(self, input_data)


@app.task(name="embed", bind=True)
def embed_model_task(self, input_data: str | list[str]):
    """ Embed Model Task """
    return embed_model(self, input_data)
