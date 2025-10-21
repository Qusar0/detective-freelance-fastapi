from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    PartInOrgFullTable,
    PartInOrgIndividualTable,
    PartInOrgOrganizationTable,
    PartInOrgRoleTable,
)
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from sqlalchemy.ext.asyncio import AsyncSession


class ParticipationOrganization:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных об участии физического лица в организациях и ИП.

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса по всем регионам
            list: Результат запроса по выбранным регионам
        """
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-orgs.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        all_regions: Optional[list] = []
        selected_regions: Optional[list] = []

        if response is not None:
            all_regions = response["all"]
            selected_regions = response["selected"]

        return all_regions, selected_regions

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных об участии физического лица в организациях и ИП.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Переключатель "Все регионы/Только выбранные регионы". Принимает 'selected', 'all'

        Returns:
            list: Результат запроса
        """
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-orgs.json?event=data&"
                f"search_type={search_type}&page={page}&rows={rows}&version=3")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]
        return full_data

    @staticmethod
    async def _process_participation_data(irbis_person_id: int, person_uuid: str, db: AsyncSession):
        """Обработка данных о банкротстве с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await ParticipationOrganization.get_full_data(person_uuid, page, 50, 'all')
            if not data:
                break
            full_data.extend(data)
            page += 1

        part_in_org_full = []
        for entry in full_data:
            org_data = entry.get("org_data")
            org_obj = None
            if org_data:
                address: dict = org_data.get('address_obj')
                region_id = None
                full_address = None

                if address:
                    region_code = int(address.get('region_code'))
                    region = await RegionSubjectDAO.get_region_by_code(region_code, db)
                    region_id = region.id if region else None
                    full_address = address.get('full_address')

                okved = org_data.get('okved')
                okved_name = None
                if okved:
                    okved_name = okved.get('name')

                org_obj = PartInOrgOrganizationTable(
                    name=org_data.get("name", ""),
                    inn=org_data.get("inn", ""),
                    ogrn=org_data.get("ogrn"),
                    address=full_address,
                    okved=okved_name,
                    region_id=region_id,
                )

            individual_data = entry.get("individual_data")
            individual_obj = None
            if individual_data:
                roles_data = individual_data.get("roles", [])
                roles_objs = [
                    PartInOrgRoleTable(
                        name=role.get("name", ""),
                        active=role.get("active", False),
                    )
                    for role in roles_data
                ]

                individual_obj = PartInOrgIndividualTable(
                    name=individual_data.get("name", ""),
                    inn=individual_data.get("inn", ""),
                    roles=roles_objs,
                )

            full_entry = PartInOrgFullTable(
                irbis_person_id=irbis_person_id,
                org=org_obj,
                individual=individual_obj,
            )

            part_in_org_full.append(full_entry)

        return part_in_org_full
