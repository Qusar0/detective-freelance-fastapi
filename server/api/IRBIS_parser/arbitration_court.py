from typing import Optional

import requests

from .base_irbis_init import BaseAuthIRBIS


class ArbitrationCourt(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None, birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None, passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.amount_by_name: Optional[dict] = None
        self.amount_by_inn: Optional[dict] = None

        self.full_data: Optional[list] = None

    def get_data_preview(self):
        """
        Получение превью данных об участии физического лица в арбитражных судах. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям amount_by_name и amount_by_inn

        Returns:
            dict: Результат запроса по имени.
            dict: Результат запроса по инн.
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-arbitr.json?event=preview"
        r = requests.get(link)
        response = r.json()

        result_name = result_inn = None

        if response["status"] == 1:
            result_name = response["response"]["name"]
            result_inn = response["response"]["inn"]

        self.amount_by_name = result_name
        self.amount_by_inn = result_inn

        return result_name, result_inn

    def get_full_data(self, page: int, rows: int, search_type: str):
        """
        Получение данных об участии физического лица в арбитражных судах. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Может принимать значения ['all', 'inn'] для поиска по имени и инн соответственно.

        Returns:
            list: Результат запроса
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-arbitr.json?event=data&page={page}&rows={rows}&search_type={search_type}"
        r = requests.get(link)
        response = r.json()

        full_data = None

        if response["status"] == 1:
            full_data = response["response"]["result"]

        self.full_data = full_data
        return full_data
