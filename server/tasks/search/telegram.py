from typing import Tuple

from celery import shared_task

from server.api.scripts import db_transactions
from server.api.scripts.html_work import response_tg_template
from server.api.scripts.ibhldr_script import get_groups_ibhldr_method, get_interests, get_phones, get_profiles
from server.api.scripts.tgdev_io_scripts import get_groups_tgdev_method
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import (
    get_event_loop,
)
from server.tasks.base.base import BaseSearchTask


class TelegramSearchTask(BaseSearchTask):
    def __init__(self, search_filters: Tuple):
        super().__init__(search_filters[2], 0)  # Цена не используется для Telegram поиска
        self.username = search_filters[0]
        self.tg_user_id = str(search_filters[1])
        self.methods_type = search_filters[4]

    async def _process_search(self, db):
        interests_html, groups1_html, groups2_html, profiles_html, phones_html = '', '', '', '', ''

        if 'interests' in self.methods_type:
            try:
                interests_html = get_interests(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'groups_1' in self.methods_type:
            try:
                groups1_html = get_groups_ibhldr_method(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'groups_2' in self.methods_type:
            try:
                groups2_html = get_groups_tgdev_method(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'profile_history' in self.methods_type:
            try:
                profiles_html = get_profiles(self.tg_user_id)
            except Exception as e:
                print(e)

        if "phone_number" in self.methods_type:
            try:
                phones_html = get_phones(self.tg_user_id)
            except Exception as e:
                print(e)

        html = response_tg_template(
            self.username + "ID" + self.tg_user_id if self.username != "" else self.tg_user_id,
            interests_html,
            groups1_html,
            groups2_html,
            profiles_html,
            phones_html,
        )

        file_storage = FileStorageService()

        await db_transactions.save_html(html, self.query_id, db, file_storage)


@shared_task(bind=True, acks_late=True)
def start_search_by_telegram(self, search_filters):
    loop = get_event_loop()
    task = TelegramSearchTask(search_filters)
    loop.run_until_complete(task.execute())
