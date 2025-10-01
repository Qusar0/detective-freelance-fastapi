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

        full_data: Optional[list] = [
            {
                "reg_date": "2018-04-03T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Михаил Васильевич Воронин",
                            "id": 972975,
                            "birth_date": "1969-05-26T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2018-002-172651-117",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ВЛАДБИЗНЕСБАНК\"",
                            "id": 1488583
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356883,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "X7LHSRGAN59375885"
                    }
                ],
                "id": 1260975,
                "pledge_type": "Движимое имущество",
                "uuid": "7090b6c9-a3d5-47d7-95b3-ae031950b9ac"
            }
        ]

        if response is not None:
            full_data = response["payload"]

        return full_data
