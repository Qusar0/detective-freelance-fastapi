import os
import time
import aiofiles
import datetime
import threading
from loguru import logger


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
