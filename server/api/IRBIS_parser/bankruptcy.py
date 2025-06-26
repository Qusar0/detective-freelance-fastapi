from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class Bankruptcy:
    def __init__(self):
        self.amount_by_name: Optional[int] = 0
        self.amount_by_inn: Optional[int] = 0

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str):
        """
        Получение превью данных о банкротстве физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям amount_by_name и amount_by_inn

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса по имени.
            int: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-bankrot.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.amount_by_name = response["name"]
            self.amount_by_inn = response["inn"]

        return self.amount_by_name, self.amount_by_inn

    async def get_full_data(self, person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных о банкротстве физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Принимает значения 'name', 'inn'

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-bankrot.json?event=data&"
                f"page={page}&rows={rows}&search_type={search_type}&version=2")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
