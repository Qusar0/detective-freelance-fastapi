from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class FSSP:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных об исполнительных производствах, связанных с физическим лицом.

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-fssp.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        fssp_preview: Optional[list] = []

        if response is not None:
            fssp_preview = response

        return fssp_preview

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int):  # noqa: WPS615
        """
        Получение данных об исполнительных производствах, связанных с физическим лицом.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-fssp.json?event=data&"
                f"page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data
