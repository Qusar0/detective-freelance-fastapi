from typing import Optional

import requests

from .base_irbis_init import BaseAuthIRBIS


class ParticipationOrganization(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None, birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None, passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.all_regions: Optional[list] = []
        self.selected_regions: Optional[list] = []

        self.full_data: Optional[list] = []

    def get_data_preview(self):
        """
        Получение превью данных об участии физического лица в организациях и ИП. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям all_regions и selected_regions

        Returns:
            list: Результат запроса по всем регионам
            list: Результат запроса по выбранным регионам
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-orgs.json?event=preview"
        response = self.get_response(link)

        if response is not None:
            self.all_regions = response["all"]
            self.selected_regions = response["selected"]

        return self.all_regions, self.selected_regions

    def get_full_data(self, page: int, rows: int, search_type: str):
        """
        Получение данных об участии физического лица в организациях и ИП. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю "Все регионы/Тольковыбранные регионы". Принимает одно из следующих значенйи ['selected', 'all']

        Returns:
            list: Результат запроса
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-orgs.json?event=data&search_type={search_type}&page={page}&rows={rows}&version=3"
        response = self.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
