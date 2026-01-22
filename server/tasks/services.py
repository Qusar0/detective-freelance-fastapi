import os
import time
import aiofiles
import datetime
import threading
import asyncio
import httpx
import redis.asyncio as redis
from server.api.conf.config import settings
from contextlib import asynccontextmanager
from loguru import logger


_redis_client = None


async def get_redis_client():
    """Получает или создает Redis клиент."""
    global _redis_client
    if _redis_client is None:
        _redis_client = await redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _redis_client


@asynccontextmanager
async def get_http_client():
    """Возвращает настроенный AsyncClient с оптимальными параметрами."""
    async with httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=20),
    ) as client:
        yield client


def update_stats(request_stats, stats_lock, attempt, success=True):
    with stats_lock:
        request_stats['total_requests'] += 1
        if success:
            if attempt == 1:
                request_stats['success_first_try'] += 1
            else:
                request_stats['success_after_retry'][attempt] += 1
        else:
            request_stats['failed_after_max_retries'] += 1


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


async def write_urls(urls, type):
    try:
        log_dir = './url_logs'
        os.makedirs(log_dir, exist_ok=True)
        logger.debug(f"Создана/проверена директория для логов: {log_dir}")

        filename = f'{log_dir}/{type}-{datetime.datetime.now()}.txt'
        logger.info(f"Запись {len(urls)} URL в файл: {filename}")

        async with aiofiles.open(filename, 'w') as f:
            for url in urls:
                await f.write(url + '\n')

        logger.success(f"Успешно записано {len(urls)} URL в файл {filename}")

    except Exception as e:
        logger.error(f"Ошибка при записи URL в файл: {e}")


def manage_threads(threads):
    try:
        active_threads = []
        max_threads = 20

        logger.debug(f"Управление {len(threads)} потоками, максимум {max_threads} одновременно")

        for i, thread in enumerate(threads):
            # Если достигнуто максимальное количество потоков, ждем, пока хотя бы один завершится
            while threading.active_count() >= max_threads:
                time.sleep(0.1)

            logger.debug(f"Запуск потока {i+1}/{len(threads)}")
            thread.start()
            active_threads.append(thread)

        logger.info("Все потоки запущены, ожидание завершения...")

        for i, thread in enumerate(active_threads):
            thread.join()
            logger.debug(f"Поток {i+1}/{len(active_threads)} завершен")
        logger.success("Все потоки успешно завершены")

    except Exception as e:
        logger.error(f"Ошибка при управлении потоками: {e}")


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
