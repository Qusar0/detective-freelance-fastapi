from celery import Celery
from server.api.conf.config import settings


def create_celery() -> Celery:
    new_celery_app = Celery(
        "ias_detective",
        broker=settings.redis_url,
        backend=settings.redis_url,
    )

    new_celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )

    new_celery_app.autodiscover_tasks(['server.celery_tasks'])

    return new_celery_app
