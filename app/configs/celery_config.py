import os
from celery import Celery

CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', 6379)}/0"

celery_client = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)
