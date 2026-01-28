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
        timeout=30.0,
        limits=httpx.Limits(
            max_keepalive_connections=20,
            max_connections=20,
        ),
    ) as client:
        yield client


SEARCH_LIMITS = {
    "google": 20,
    "yandex": 7,
}

google_semaphore = asyncio.Semaphore(SEARCH_LIMITS["google"])
yandex_semaphore = asyncio.Semaphore(SEARCH_LIMITS["yandex"])


def _get_semaphore(engine: str) -> asyncio.Semaphore:
    if engine == "google":
        return google_semaphore
    elif engine == "yandex":
        return yandex_semaphore
    else:
        raise ValueError(f"Unknown engine: {engine}")


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


async def run_with_engine_limit(task, task_id: int):
    engine = _detect_engine_from_task(task)
    semaphore = _get_semaphore(engine)

    async with semaphore:
        logger.info(
            f"Задача {task_id} → {engine} "
            f"(active: {SEARCH_LIMITS[engine] - semaphore._value}/"
            f"{SEARCH_LIMITS[engine]})"
        )
        return await task


def _detect_engine_from_task(task):
    """Определяет search engine из задачи.

    Пытается получить информацию о task из его closure переменных.
    По умолчанию возвращает 'google'.
    """
    try:
        if hasattr(task, 'cr_frame') and task.cr_frame:
            frame_locals = task.cr_frame.f_locals
            if 'input_data' in frame_locals:
                input_data = frame_locals['input_data']
                if isinstance(input_data, tuple) and len(input_data) > 0:
                    url = input_data[0]
                    if 'search_yandex' in url or 'yandex' in url.lower():
                        return 'yandex'
    except Exception as e:
        logger.debug(f"Не удалось определить engine из задачи: {e}")

    return "google"


async def manage_async_tasks(tasks):
    wrapped_tasks = [
        run_with_engine_limit(task, i)
        for i, task in enumerate(tasks)
    ]

    results = await asyncio.gather(
        *wrapped_tasks,
        return_exceptions=True,
    )

    logger.success(f"Завершено задач: {len(results)}")
    return results


async def write_urls(urls, type_name: str):
    try:
        log_dir = "./url_logs"
        os.makedirs(log_dir, exist_ok=True)

        filename = f'{log_dir}/{type}-{datetime.datetime.now()}.txt'
        logger.info(f"Запись {len(urls)} URL в файл: {filename}")

        async with aiofiles.open(filename, 'w') as f:
            for url in urls:
                await f.write(url + '\n')

        logger.success(f"Успешно записано {len(urls)} URL в файл {filename}")

    except Exception as e:
        logger.error(f"Ошибка при записи URL: {e}")
