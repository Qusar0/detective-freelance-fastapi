from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class Deposits:
    def __init__(self):
        self.preview_data: Optional[list] = []

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str):
        """
        Получение превью данных о залогах (движимого имущества) физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям preview_data

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-pledge.json?event=preview-type")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.preview_data = response

        return self.preview_data

    async def get_full_data(self, person_uuid: str, page: int, rows: int):
        """
        Получение данных о залогах (движимого имущества) физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-pledge.json?event=data"
                f"&page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
