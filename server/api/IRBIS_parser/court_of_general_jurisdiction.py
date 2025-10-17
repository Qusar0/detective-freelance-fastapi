from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from server.api.dao.irbis.process_type import ProcessTypeDAO
from server.api.models.irbis_models import (
    CourtGeneralFacesTable,
    CourtGeneralProgressTable,
    CourtGeneralJurFullTable,
    MatchType,
)
from loguru import logger


class CourtGeneralJurisdiction:
    @staticmethod
    async def get_data_preview(person_uuid: str, filter_text: str, strategy: str):
        """
        Получение превью данных о судебных делах физического лица.

        Args:
            person_uuid (str): uuid человека
            filter_text (str): Соответствует значению в поле "Поиск".
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']  # noqa: E501

        Returns:
            dict: Результат запроса.
        """
        logger.info(
            f"Запрос превью данных для person_uuid: {person_uuid}, filter_text: {filter_text}, strategy: {strategy}",
        )

        link = (
            f"https://ir-bis.org/ru/base/-/services/report/"
            f"{person_uuid}/people-judge.json?event=role-preview"
            f"&filter_text={filter_text}&strategy={strategy}"
        )

        try:
            response = await BaseAuthIRBIS.get_response(link)
            logger.debug(f"Получен ответ превью данных, статус: {response is not None}")

            full_data: Optional[dict] = dict()
            short_data: Optional[dict] = dict()

            if response is not None:
                full_data = response["full"]
                short_data = response["short"]
                logger.info(
                    f"Превью данных получено: full - {len(full_data)} записей, short - {len(short_data)} записей",
                )

            return full_data, short_data

        except Exception as e:
            logger.error(f"Ошибка при получении превью данных для {person_uuid}: {e}")
            return dict(), dict()

    @staticmethod
    async def get_category_result(person_uuid: str, filter0: str, filter_text: str, strategy: str):
        """
        Получение данных о категориях судебных дел физического лица.

        Args:
            person_uuid (str): uuid человека
            filter0 (str): Соответствует переключателю 'Все данные/Полное совпадение/Частичное совпадение'. Принимает одно из следующих значенйи ['allData', 'full', 'partly']  # noqa: E501
            filter_text (str): Соответствует значению в поле "Поиск".
            strategy (str): Соответствует переключателю "по выбранным регионам / по ВСЕМ регионам". Принимает одно из следующих значенйи ['selected', 'all']  # noqa: E501

        Returns:
            dict: Результат запроса.
        """
        logger.info(
            f"Запрос категорий дел для person_uuid: {person_uuid}, filter0: {filter0}, filter_text: {filter_text}",
        )

        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=category-preview&"
                f"filter0={filter0}&filter_text={filter_text}&strategy={strategy}")

        try:
            response = await BaseAuthIRBIS.get_response(link)
            logger.debug(f"Получен ответ категорий дел, статус: {response is not None}")

            category: Optional[dict] = dict()
            result_response = dict()

            if response is not None:
                for data_response in response:
                    result_response[data_response["type"]] = data_response["count"]
                logger.info(f"Категории дел получены: {len(result_response)} категорий")

            category = result_response
            return category

        except Exception as e:
            logger.error(f"Ошибка при получении категорий дел для {person_uuid}: {e}")
            return dict()

    @staticmethod
    async def get_full_data(  # noqa: WPS615, WPS211
        person_uuid: str,
        page: int,
        rows: int,
        strategy: str,
        filter0: str,
        filter_text: str,
    ):
        """
        Получение данных об участии физического лица в арбитражных судах.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            strategy (str): Переключатель "По выбранным регионам / по ВСЕМ регионам". Может принимать значения ['selected', 'all']  # noqa: E501
            filter0 (str): Переключатель "Все данные/Полное совпадение/Частичное совпадение". Может принимать значения ['allData', 'full', 'partly']  # noqa: E501
            filter_text (str): Соответствует значению в поле "Поиск"

        Returns:
            list: Результат запроса
        """
        logger.debug(f"Запрос полных данных страница {page} для {person_uuid}, filter0: {filter0}")

        link = (f"https://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=role-data&version=2"
                f"&page={page}&rows={rows}&strategy={strategy}"
                f"&filter0={filter0}&filter_text={filter_text}")

        try:
            response = await BaseAuthIRBIS.get_response(link)

            full_data: Optional[list] = []
            if response is not None:
                full_data = response["result"]
                logger.debug(f"Страница {page} получена: {len(full_data)} записей")

            return full_data

        except Exception as e:
            logger.error(f"Ошибка при получении полных данных страница {page} для {person_uuid}: {e}")
            return []

    @staticmethod
    async def _process_court_cases(irbis_person_id: int, person_uuid: str, match_type: MatchType, db: AsyncSession):
        """Обрабатывает данные судебных дел для указанного типа фильтра."""
        logger.info(
            f"Начало обработки судебных дел для irbis_person_id: {irbis_person_id}, match_type: {match_type.name}",
        )

        court_gen_full = []
        page = 1
        full_data = ['']
        total_cases_processed = 0

        try:
            regions_map = await RegionSubjectDAO.get_regions_map(db)
            process_types_map = await ProcessTypeDAO.get_process_types_map(db)

            while full_data:
                logger.debug(f"Запрос страницы {page} для match_type: {match_type.name}")

                full_data = await CourtGeneralJurisdiction.get_full_data(
                    person_uuid=person_uuid,
                    page=page,
                    rows=100,
                    filter0=match_type.name,
                    filter_text='',
                    strategy='all'
                )

                if not full_data:
                    logger.debug(f"Пустая страница {page}, завершение обработки для match_type: {match_type.name}")
                    break

                for case_data in full_data:
                    try:
                        header_data = case_data.get("header", {})

                        faces_data = case_data.get("faces", [])
                        faces = [
                            CourtGeneralFacesTable(
                                role=face.get("role"),
                                role_name=face.get("role_name"),
                                face=face.get("face"),
                                papers=", ".join(map(str, face.get("papers", []))),
                                papers_pretty=", ".join(map(str, face.get("papers_pretty", [])))
                            )
                            for face in faces_data
                        ]

                        progress_data = case_data.get("case_progress", [])
                        progress = [
                            CourtGeneralProgressTable(
                                name=pr.get("name"),
                                progress_date=pr.get("date"),
                                resolution=pr.get("resolution")
                            )
                            for pr in progress_data
                        ]

                        region_code = header_data.get("region")
                        region = regions_map.get(region_code)
                        if not region:
                            logger.warning(f"Регион с кодом {region_code} не найден в БД")

                        process_type_code = header_data.get("process_type")
                        process_type = process_types_map.get(process_type_code)
                        if not process_type:
                            logger.warning(f"Тип процесса с кодом {process_type_code} не найден в БД")

                        case = CourtGeneralJurFullTable(
                            irbis_person_id=irbis_person_id,
                            faces=faces,
                            progress=progress,
                            case_number=header_data.get("case_number"),
                            region_id=region.id if region else None,
                            court_name=header_data.get("court_name"),
                            process_type_id=process_type.id if process_type else None,
                            start_date=header_data.get("start_date"),
                            end_date=header_data.get("end_date") or "to date",
                            review=header_data.get("review"),
                            judge=header_data.get("judge"),
                            articles=header_data.get("articles", []),
                            papers=", ".join(map(str, header_data.get("papers", []))),
                            papers_pretty=", ".join(map(str, header_data.get("papers_pretty", []))),
                            links=header_data.get("links", {}),
                            match_type_id=match_type.id,
                        )
                        court_gen_full.append(case)
                        total_cases_processed += 1

                    except Exception as e:
                        logger.error(f"Ошибка при обработке дела на странице {page}: {e}")
                        continue
                page += 1

            logger.info(
                f"Завершена обработка для match_type: {match_type.name}, обработано дел: {total_cases_processed}",
            )
            return court_gen_full
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке судебных дел для {irbis_person_id}: {e}")
            return []
