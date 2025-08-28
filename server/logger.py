import os
from loguru import logger
import logging
import threading
import datetime


log_file = os.getenv("LOG_FILE", "logs/debug.log")
logger.add(
    log_file,
    level="DEBUG",
    format="{level} | {time} | {function}:{line} | {message}",
    rotation="4096 KB",
    compression="zip",
    enqueue=True,
)

logging.getLogger('sqlalchemy.engine.Engine').disabled = True


class SearchLogger:
    def __init__(self, query_id, log_file="search_errors.log"):
        self.query_id = query_id
        self.log_file = log_file
        self.lock = threading.Lock()

    def log_error(self, error_message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [ID:{self.query_id}] ОШИБКА: {error_message}\n"

        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
