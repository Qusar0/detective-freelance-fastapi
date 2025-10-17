from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class MLIndex:
    @staticmethod
    async def get_full_data(person_uuid: str):  # noqa: WPS615
        """
        Получение значения ML-индекса данного физического лица.

        Args:
            person_uuid (str): uuid человека

        Returns:
            dict: Результат запроса
        """
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-scoring.json?event=scoring")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: dict = dict()

        if response is not None:
            full_data = response

        return full_data
