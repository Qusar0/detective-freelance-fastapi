from celery import Celery
from loguru import logger
from server.api.conf.config import settings
import os


def create_celery() -> Celery:
    logger.info("Создание Celery приложения")
    logger.debug(f"Redis URL: {settings.redis_url}")

    celery_app = Celery(
        "ias_detective",
        broker=settings.redis_url,
        backend=settings.redis_url,
        broker_connection_retry_on_startup=True,
    )
    logger.debug("Celery приложение создано")

    celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )
    logger.debug("Конфигурация Celery обновлена")

    task_name = os.getenv("TASK", "")

    task_modules = ["server.tasks.base.base", f"server.tasks.search.{task_name}"]
    logger.info(f"Задачи для загрузки: {task_modules}")
    celery_app.autodiscover_tasks(task_modules)

    logger.success("Celery приложение успешно инициализировано")
    return celery_app


celery_app = create_celery()
logger.success("Celery приложение готово к работе")
