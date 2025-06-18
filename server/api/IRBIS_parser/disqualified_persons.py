from typing import Optional

import requests

from .base_irbis_init import BaseAuthIRBIS


class DisqualifiedPersons(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None, birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None, passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.count: Optional[int] = None

        self.full_data: Optional[list] = None

    def get_data_preview(self):
        """
        Получение превью данных о дисквалификации физического лица.. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям count

        Returns:
            int: Результат запроса
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-disqualified.json?event=preview"
        r = requests.get(link)
        response = r.json()

        count = None

        if response["status"] == 1:
            count = response["response"]

        self.count = count

        return count

    def get_full_data(self, page: int, rows: int):
        """
        Получение данных о дисквалификации физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-disqualified.json?event=data&page={page}&rows={rows}"
        r = requests.get(link)
        response = r.json()

        full_data = None

        if response["status"] == 1:
            full_data = response["response"]["result"]

        self.full_data = full_data
        return full_data
