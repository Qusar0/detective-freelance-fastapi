from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class TerrorList:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о нахождении физического лица в списке террористов и экстремистов.

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-terrorist.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        count: Optional[int] = 0

        if response is not None:
            count = response

        return count

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int):  # noqa: WPS615
        """
        Получение данных о нахождении физического лица в списке террористов и экстремистов.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-terrorist.json?event=data&"
                f"page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data
