from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class Pledges:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о залогах (движимого имущества) физического лица.

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-pledge.json?event=preview-type")
        response = await BaseAuthIRBIS.get_response(link)

        preview_data: Optional[list] = []

        if response is not None:
            preview_data = response

        return preview_data

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int):  # noqa: WPS615
        """
        Получение данных о залогах (движимого имущества) физического лица.

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

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data
