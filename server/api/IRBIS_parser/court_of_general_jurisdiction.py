from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class CourtGeneralJurisdiction:
    def __init__(self):
        self.full_fio_data_preview: Optional[dict] = dict()
        self.short_fio_data_preview: Optional[dict] = dict()

        self.category: Optional[dict] = dict()

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str, filter_text: str, strategy: str):
        """
            Получение превью данных о судебных делах физического лица. Использовать повторно функцию для обновления данных.
            Если нужны предыдущие, необходимо обратиться к полям full_fio_data_preview и short_fio_data_preview

            Args:
                person_uuid (str): uuid человека
                filter_text (str): Соответствует значению в поле "Поиск".
                strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']

            Returns:
                dict: Результат запроса.
            """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=role-preview"
                f"&filter_text={filter_text}&strategy={strategy}")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_fio_data_preview = response["full"]
            self.short_fio_data_preview = response["short"]

        return self.full_fio_data_preview, self.short_fio_data_preview

    async def get_category_result(self, person_uuid: str, filter0: str, filter_text: str, strategy: str):
        """
        Получение данных о категориях судебных дел физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полю category

        Args:
            person_uuid (str): uuid человека
            filter0 (str): Соответствует переключателю 'Все данные/Полное совпадение/Частичное совпадение'. Принимает одно из следующих значенйи ['allData', 'full', 'partly']
            filter_text (str): Соответствует значению в поле "Поиск".
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']

        Returns:
            dict: Результат запроса.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=categorypreview&"
                f"filter0={filter0}&filter_text={filter_text}&strategy={strategy}")
        response = await BaseAuthIRBIS.get_response(link)

        result_response = dict()
        if response is not None:
            for data_response in response:
                result_response[data_response["type"]] = data_response["count"]

        self.category = result_response
        return self.category

    async def get_full_data(self, person_uuid: str, page: int, rows: int, strategy: str, filter0: str, filter_text: str):
        """
        Получение данных об участии физического лица в арбитражных судах. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Может принимать значения ['selected', 'all']
            filter0 (str): Соответствует переключателю "Все данные/Полное совпадение/Частичное совпадение". Может принимать значения ['allData', 'full', 'partly']
            filter_text (str): Соответствует значению в поле "Поиск"

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=roledata&version=2"
                f"&page={page}&rows={rows}&strategy={strategy}"
                f"&filter0={filter0}&filter_text={filter_text}")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
