from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class TaxArrears:
    @staticmethod
    async def get_full_data(person_uuid: str):  # noqa: WPS615
        """
        Получение данных о налоговых задолженностях физического лица.

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-nalog.json?event=data")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["payload"]

        return full_data
