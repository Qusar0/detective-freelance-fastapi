import os
import time
import aiofiles
import datetime
import threading


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
    log_dir = './url_logs'
    os.makedirs(log_dir, exist_ok=True)

    filename = f'{log_dir}/{type}-{datetime.datetime.now()}.txt'
    async with aiofiles.open(filename, 'w') as f:
        for url in urls:
            await f.write(url + '\n')


def manage_threads(threads):
    active_threads = []
    max_threads = 20

    for thread in threads:
        # Если достигнуто максимальное количество потоков, ждем, пока хотя бы один завершится
        while threading.active_count() >= max_threads:
            time.sleep(0.1)
        thread.start()
        active_threads.append(thread)

    for thread in active_threads:
        thread.join()
