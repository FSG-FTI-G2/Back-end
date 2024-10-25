from celery import Celery
import os

CELERY_BROKER_URL = f"redis://{os.environ.get('CELERY_HOST')}:{os.environ.get('CELERY_PORT')}/0"

app = Celery(
    'embedding_tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)

