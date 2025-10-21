from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    PledgeFullTable,
    PledgePartiesTable,
    PledgeObjectTable
)


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
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
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
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-pledge.json?event=data"
                f"&page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_pledgess_data(irbis_person_id: int, person_uuid: str):
        """Обработка данных о банкротстве с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await Pledges.get_full_data(person_uuid, page, 50)
            if not data:
                break
            full_data.extend(data)
            page += 1

        pledges_full = []
        for pledge_info in full_data:
            all_pledge_parties = []
            for pledge_type in {'pledgers', 'pledgees'}:
                info = pledge_info.get(pledge_type)
                if info:
                    for role_type in {'orgs', 'peoples'}:
                        parties = [
                            PledgePartiesTable(
                                name=party.get("name", ""),
                                type=pledge_type,
                                subtype=role_type,
                                birth_date=party.get("birth_date"),
                                inn=party.get("inn"),
                                ogrn=party.get("ogrn")
                            )
                            for party in info.get(role_type, [])
                        ]
                        all_pledge_parties.extend(parties)

            pledges = [
                PledgeObjectTable(
                    pledge_num_name=pledge.get("pledge_id_name", ""),
                    pledge_num=pledge.get("pledge_id", ""),
                    pledge_type=pledge.get("pledge_type", ""),
                )
                for pledge in pledge_info.get("pledges", [])
            ]

            obj = PledgeFullTable(
                irbis_person_id=irbis_person_id,
                reg_date=pledge_info.get('reg_date'),
                pledge_reestr_number=pledge_info.get('pledge_number'),
                pledge_type=pledge_info.get("pledge_type"),
                parties=all_pledge_parties,
                pledges=pledges,
            )
            pledges_full.append(obj)

        return pledges_full
