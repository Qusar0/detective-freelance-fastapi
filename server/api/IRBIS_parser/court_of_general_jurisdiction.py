from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class CourtGeneralJurisdiction(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None,
                 birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None,
                 passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.full_fio_data_preview: Optional[dict] = None
        self.short_fio_data_preview: Optional[dict] = None

        self.category: Optional[dict] = dict()

        self.full_data: Optional[list] = []

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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-judge.json?event=role-preview"
                f"&filter_text={filter_text}&strategy={strategy}")
        response = self.get_response(link)

        if response is not None:
            self.full_fio_data_preview = response["full"]
            self.short_fio_data_preview = response["short"]

        return self.full_fio_data_preview, self.short_fio_data_preview

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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-judge.json?event=categorypreview&"
                f"filter0={filter0}&filter_text={filter_text}&strategy={strategy}")
        response = self.get_response(link)

        result = dict()
        if response is not None:
            for data in response:
                result[data["type"]] = data["count"]

        self.category = result
        return self.category

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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-judge.json?event=roledata&version=2"
                f"&page={page}&rows={rows}&strategy={strategy}"
                f"&filter0={filter0}&filter_text={filter_text}")
        response = self.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
