from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class Bankruptcy:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о банкротстве физического лица.


        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса по имени.
            int: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-bankrot.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        amount_by_name: Optional[int] = 0
        amount_by_inn: Optional[int] = 0

        if response is not None:
            amount_by_name = response["name"]
            amount_by_inn = response["inn"]

        return amount_by_name, amount_by_inn

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных о банкротстве физического лица.

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

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data
