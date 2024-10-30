from celery import Celery

CELERY_BROKER_URL = "redis://localhost:6379/0"

celery_client = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)
