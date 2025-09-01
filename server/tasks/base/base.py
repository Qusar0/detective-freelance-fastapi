from loguru import logger
import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from threading import Lock

from server.api.dao.user_queries import UserQueriesDAO
from server.api.dao.telegram_notifications import TelegramNorificationsDAO
from server.api.dao.balance_history import BalanceHistoryDAO
from server.api.scripts.sse_manager import generate_sse_message_type, send_sse_notification
from server.bots.notification_bot import send_notification
from server.api.database.database import async_session


class BaseSearchTask(ABC):
    def __init__(self, query_id: int, price: float):
        self.query_id = query_id
        self.price = price
        self.user_id = None
        self.money_to_return = 0
        self.request_stats = {
            'total_requests': 0,
            'success_first_try': 0,
            'success_after_retry': defaultdict(int),
            'failed_after_max_retries': 0,
        }
        self.stats_lock = Lock()

    async def execute(self):
        async with async_session() as db:
            user_query = await UserQueriesDAO.get_user_query(self.query_id, db)
            if user_query.query_status == "done":
                return

            self.user_id = user_query.user_id

            try:
                await self._process_search(db)
                await self._handle_success(user_query, db)
            except Exception as e:
                logger.error(f"Error has occurred in task: {str(e)}")
                #print(e)
                await self._handle_error(user_query, db)
            finally:
                await self._update_balances(db)

    @abstractmethod
    async def _process_search(self, db):
        pass

    async def _handle_success(self, user_query, db):
        channel = await generate_sse_message_type(user_id=self.user_id, db=db)
        await UserQueriesDAO.change_query_status(user_query, "done", db)
        await send_sse_notification(user_query, channel, db)

        chat_id = await TelegramNorificationsDAO.is_user_subscribed_on_tg(self.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title)

    async def _handle_error(self, user_query, db):
        channel = await generate_sse_message_type(user_id=self.user_id, db=db)
        await UserQueriesDAO.change_query_status(user_query, "failed", db)
        await send_sse_notification(user_query, channel, db)

        if self.money_to_return > 0:
            await BalanceHistoryDAO.return_balance(
                self.user_id,
                user_query.query_id,
                self.money_to_return,
                channel,
                db,
            )

    @abstractmethod
    async def _update_balances(self, db):
        pass

    def save_stats_to_file(self, filename="search_stats.txt"):
        """Сохраняет статистику запросов в файл с русскоязычным выводом и ID запроса"""
        with self.stats_lock:
            total = self.request_stats['total_requests']
            if total == 0:
                return "Не было выполнено ни одного запроса."

            stats_text = [
                f"=== СТАТИСТИКА ЗАПРОСА ID: {self.query_id} ===",
                f"Общее количество запросов: {total}",
                f"Успешно с 1 попытки: \
                {self.request_stats['success_first_try']} \
                ({self.request_stats['success_first_try'] / total * 100:.1f}%)",

                *[
                    f"Успешно после {attempt} попыток: {count} ({count / total * 100:.1f}%)"
                    for attempt, count in sorted(
                        self.request_stats['success_after_retry'].items()
                    )
                ],

                f"Не удалось после всех попыток: \
                {self.request_stats['failed_after_max_retries']} \
                ({self.request_stats['failed_after_max_retries'] / total * 100:.1f}%)",
                f"Время формирования отчета: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "===================================="
            ]

            with open(filename, "a", encoding="utf-8") as f:
                f.write("\n".join(stats_text) + "\n\n")
