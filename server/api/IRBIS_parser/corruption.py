from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class Corruption:
    def __init__(self):
        self.count: Optional[int] = 0

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str):
        """
        Получение превью данных о причастии к коррупционной деятельности физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям count

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-corrupt.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.count = response["count"]

        return self.count

    async def get_full_data(self, person_uuid: str, page: int, rows: int):
        """
        Получение данных о причастии к коррупционной деятельности физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-corrupt.json?event=data&"
                f"page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
