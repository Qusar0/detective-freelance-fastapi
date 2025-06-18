from typing import Optional

import requests

from .base_irbis_init import BaseAuthIRBIS


class CourtGeneralJurisdiction(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None, birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None, passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.full_fio_data_preview: Optional[dict] = None
        self.short_fio_data_preview: Optional[dict] = None

        self.category: Optional[dict] = None

        self.full_data: Optional[list] = None

    def get_data_preview(self, filter_text: str, strategy: str):
        """
            Получение превью данных о судебных делах физического лица. Использовать повторно функцию для обновления данных.
            Если нужны предыдущие, необходимо обратиться к полям full_fio_data_preview и short_fio_data_preview

            Args:
                filter_text (str): Соответствует значению в поле "Поиск".
                strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']

            Returns:
                dict: Результат запроса.
            """
        link = (f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-judge.json?event=role-preview"
                f"&filter_text={filter_text}&strategy={strategy}")
        r = requests.get(link)
        response = r.json()

        result_full = result_short = None

        if response["status"] == 1:
            result_full = response["response"]["full"]
            result_short = response["response"]["short"]

        self.full_fio_data_preview = result_full
        self.short_fio_data_preview = result_short

        return result_full, result_short

    def get_category_result(self, filter0: str, filter_text: str, strategy: str):
        """
        Получение данных о категориях судебных дел физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полю category

        Args:
            filter0 (str): Соответствует переключателю 'Все данные/Полное совпадение/Частичное совпадение'. Принимает одно из следующих значенйи ['allData', 'full', 'partly']
            filter_text (str): Соответствует значению в поле "Поиск".
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']

        Returns:
            dict: Результат запроса.
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-judge.json?event=categorypreview&filter0={filter0}&filter_text={filter_text}&strategy={strategy}"
        r = requests.get(link)
        response = r.json()

        result = dict()
        if response["status"] == 1:
            for data in response["response"]:
                result[data["type"]] = data["count"]

        self.category = result
        return result

    def get_full_data(self, page: int, rows: int, strategy: str, filter0: str, filter_text: str):
        """
        Получение данных об участии физического лица в арбитражных судах. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Может принимать значения ['selected', 'all'] соответственно.
            filter0 (str): Соответствует переключателю "Все данные/Полное совпадение/Частичное совпадение". Может принимать значения ['allData', 'full', 'partly'] соответственно.
            filter_text (str): Соответствует значению в поле "Поиск"

        Returns:
            list: Результат запроса
        """
        link = f"http://ir-bis.org/ru/base/-/services/report/{self.person_uuid}/people-judge.json?event=roledata&version=2&page={page}&rows={rows}&strategy={strategy}&filter0={filter0}&filter_text={filter_text}"
        r = requests.get(link)
        response = r.json()

        full_data = None

        if response["status"] == 1:
            full_data = response["response"]["result"]

        self.full_data = full_data
        return full_data
