from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class ArbitrationCourt:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных об участии физического лица в арбитражных судах.

        Args:
            person_uuid (str): uuid человека

        Returns:
            dict: Результат запроса по имени.
            dict: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-arbitr.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        amount_by_name: Optional[dict] = dict()
        amount_by_inn: Optional[dict] = dict()

        if response is not None:
            amount_by_name = response["name"]
            amount_by_inn = response["inn"]

        return amount_by_name, amount_by_inn

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных об участии физического лица в арбитражных судах.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Принимает значения 'all', 'inn'

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-arbitr.json?event=data&page={page}"
                f"&rows={rows}&search_type={search_type}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data
