from typing import Optional
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    ArbitrationCourtFullTable,
    ArbitrationCourtOpponents,
)
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from server.api.dao.irbis.arbitration_court_case_types import ArbitrationCourtCaseTypesDAO
from server.api.dao.irbis.person_role_type import PersonRoleTypeDAO


class ArbitrationCourt:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных об участии физического лица в арбитражных судах.

        Args:
            person_uuid (str): uuid человека

        Returns:
            dict: Результат запроса по имени.
            dict: Результат запроса по инн.
        """
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-arbitr.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        amount_by_name: Optional[dict] = dict()
        amount_by_inn: Optional[dict] = dict()

        if response is not None:
            amount_by_name = response["name"]
            amount_by_inn = response["inn"]

        return amount_by_name, amount_by_inn

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):
        """
        Получение данных об участии физического лица в арбитражных судах.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Принимает значения 'all', 'inn'

        Returns:
            list: Результат запроса
        """
        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-arbitr.json?event=data&page={page}"
                f"&rows={rows}&search_type={search_type}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_arbitration_cases(irbis_person_id: int, person_uuid: str, search_type: str, db: AsyncSession):
        """Обрабатывает данные арбитражных дел."""
        logger.info(
            f"Начало обработки арбитражных дел для irbis_person_id: {irbis_person_id}, тип поиска: {search_type}",
        )

        arbitration_court_full = []
        page = 1
        full_data = ['']
        total_cases_processed = 0
        search_type_for_db = search_type if search_type == 'inn' else 'name'

        try:
            regions_map = await RegionSubjectDAO.get_regions_map(db)
            case_types_map = await ArbitrationCourtCaseTypesDAO.get_case_types_map(db)
            person_roles_map = await PersonRoleTypeDAO.get_roles_with_short_map(db)

            while full_data:
                logger.debug(f"Запрос страницы {page} для типа поиска: {search_type}")

                full_data = await ArbitrationCourt.get_full_data(
                    person_uuid=person_uuid,
                    page=page,
                    rows=100,
                    search_type=search_type
                )

                if not full_data:
                    logger.debug(f"Пустая страница {page}, завершение обработки для типа поиска: {search_type}")
                    break

                for case_data in full_data:
                    try:
                        regions = case_data['regions']
                        region_code = regions[0] if regions else 0
                        region = regions_map.get(region_code)
                        region_id = region.id if region else None

                        case_type_response = case_data['case_type']
                        case_type_code = case_type_response if case_type_response else 0
                        case_type = case_types_map.get(case_type_code)
                        case_type_id = case_type.id if case_type else None

                        oponents = [
                            ArbitrationCourtOpponents(name=opponent_name)
                            for opponent_name in case_data.get('opponent_names', [])
                        ]

                        case = ArbitrationCourtFullTable(
                            irbis_person_id=irbis_person_id,
                            court_name_val=case_data.get("court_name_val"),
                            role=person_roles_map.get(case_data.get("role")),
                            case_date=case_data.get("case_date"),
                            case_id=case_data.get("case_id"),
                            inn=case_data.get("inn"),
                            name=case_data.get("name"),
                            case_type_id=case_type_id,
                            address_val=case_data.get("address_val"),
                            region_id=region_id,
                            case_number=case_data.get('case_number'),
                            oponents=oponents,
                            search_type=search_type_for_db,
                        )
                        arbitration_court_full.append(case)
                        total_cases_processed += 1
                    except Exception as e:
                        logger.error(f"Ошибка при обработке дела на странице {page}: {e}")
                        continue
                page += 1

            logger.info(
                f"Завершена обработка для типа поиска: {search_type}, обработано дел: {total_cases_processed}",
            )
            return arbitration_court_full
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке судебных дел для {irbis_person_id}: {e}")
            return []
