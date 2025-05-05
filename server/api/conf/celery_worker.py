from celery import Celery


def create_celery() -> Celery:
    celery_app = Celery(
        "ias_detective",
        broker="redis://:1@localhost:6379",
        backend="redis://:1@localhost:6379",
    )

    celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )

    celery_app.autodiscover_tasks(['server.celery_tasks'])

    return celery_app


celery_app = create_celery()
