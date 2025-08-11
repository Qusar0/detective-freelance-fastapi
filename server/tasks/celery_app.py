from celery import Celery

from server.api.conf.config import settings
import logging


logging.getLogger('sqlalchemy.engine.Engine').disabled = True


def create_celery() -> Celery:
    celery_app = Celery(
        "ias_detective",
        broker=settings.redis_url,
        backend=settings.redis_url,
    )

    celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )

    celery_app.autodiscover_tasks([
        'server.tasks.base.base',
        'server.tasks.search.company',
        'server.tasks.search.email',
        'server.tasks.search.name',
        'server.tasks.search.number',
        'server.tasks.search.telegram',
        'server.tasks.search.irbis'
    ])

    return celery_app


celery_app = create_celery()
