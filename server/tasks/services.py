import os
import asyncio
import datetime
import aiofiles
import httpx
import redis.asyncio as redis

from loguru import logger
from contextlib import asynccontextmanager
from server.api.conf.config import settings


_redis_client = None


async def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _redis_client


@asynccontextmanager
async def get_http_client():
    async with httpx.AsyncClient(
        timeout=60.0,
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=20),
    ) as client:
        yield client


async def update_stats_async(request_stats, stats_lock, attempt, success=True):
    async with stats_lock:
        request_stats['total_requests'] += 1
        if success:
            if attempt == 1:
                request_stats['success_first_try'] += 1
            else:
                request_stats['success_after_retry'][attempt] += 1
        else:
            request_stats['failed_after_max_retries'] += 1


async def write_urls(urls, type_name: str):
    try:
        log_dir = "./url_logs"
        os.makedirs(log_dir, exist_ok=True)

        filename = f'{log_dir}/{type_name}-{datetime.datetime.now()}.txt'
        logger.info(f"Запись {len(urls)} URL в файл: {filename}")

        async with aiofiles.open(filename, 'w') as f:
            for url in urls:
                await f.write(url + '\n')

        logger.success(f"Успешно записано {len(urls)} URL в файл {filename}")

    except Exception as e:
        logger.error(f"Ошибка при записи URL в файл: {e}")


async def manage_async_tasks(tasks, max_concurrent=20):
    """Управляет выполнением асинхронных задач с ограничением параллелизма.

    Использует Redis для ограничения одновременных задач до 20 для всех сервисов вместе.
    """
    try:
        redis_client = await get_redis_client()
        semaphore_key = "global_task_semaphore"
        max_slots = max_concurrent

        async def run_with_redis_semaphore(task, task_id):
            """Выполняет задачу с получением слота из Redis."""
            while True:
                current_count = await redis_client.incr(semaphore_key)
                if current_count <= max_slots:
                    break
                await redis_client.decr(semaphore_key)
                await asyncio.sleep(0.1)

            try:
                logger.debug(f"Задача {task_id} запущена. Активных задач: {current_count}/{max_slots}")
                return await task
            finally:
                await redis_client.decr(semaphore_key)
                logger.debug(f"Задача {task_id} завершена. Слот освобожден")

        task_list = [run_with_redis_semaphore(task, i) for i, task in enumerate(tasks)]
        results = await asyncio.gather(*task_list, return_exceptions=True)

        logger.success(f"Все {len(tasks)} задач успешно завершены")
        return results

    except Exception as e:
        logger.error(f"Ошибка при управлении асинхронными задачами: {e}")
        raise


async def get_search_engine_semaphores():
    """Возвращает семафоры для каждой поисковой системы.

    Google: 20 одновременных запросов
    Yandex: 10 одновременных запросов
    """
    redis_client = await get_redis_client()
    return {
        'google': {
            'redis_client': redis_client,
            'key': 'google_task_semaphore',
            'max_slots': 20,
        },
        'yandex': {
            'redis_client': redis_client,
            'key': 'yandex_task_semaphore',
            'max_slots': 10,
        },
    }


async def acquire_search_engine_semaphore(semaphore_key: str, semaphore_config: dict):
    """Получает слот семафора для поисковой системы."""
    while True:
        current_count = await semaphore_config['redis_client'].incr(semaphore_key)
        if current_count <= semaphore_config['max_slots']:
            return current_count
        await semaphore_config['redis_client'].decr(semaphore_key)
        await asyncio.sleep(0.1)


async def release_search_engine_semaphore(semaphore_key: str, redis_client):
    """Освобождает слот семафора для поисковой системы."""
    await redis_client.decr(semaphore_key)

