from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class ArbitrationCourt:
    def __init__(self):
        self.amount_by_name: Optional[dict] = dict()
        self.amount_by_inn: Optional[dict] = dict()

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str):
        """
        Получение превью данных об участии физического лица в арбитражных судах.
        Если нужны предыдущие, необходимо обратиться к полям amount_by_name и amount_by_inn

        Args:
            person_uuid (str): uuid человека

        Returns:
            dict: Результат запроса по имени.
            dict: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-arbitr.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.amount_by_name = response["name"]
            self.amount_by_inn = response["inn"]

        return self.amount_by_name, self.amount_by_inn

    async def get_full_data(self, person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных об участии физического лица в арбитражных судах.
        Если нужны предыдущие, необходимо обратиться к полям full_data

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

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
