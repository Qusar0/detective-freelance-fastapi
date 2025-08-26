from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    CourtGeneralFacesTable,
    CourtGeneralProgressTable,
    CourtGeneralJurFullTable,
    MatchType,
)


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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=role-preview"
                f"&filter_text={filter_text}&strategy={strategy}")
        response = await BaseAuthIRBIS.get_response(link)

        full_fio_data_preview: Optional[dict] = dict()
        short_fio_data_preview: Optional[dict] = dict()

        if response is not None:
            full_fio_data_preview = response["full"]
            short_fio_data_preview = response["short"]

        return full_fio_data_preview, short_fio_data_preview

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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=category-preview&"
                f"filter0={filter0}&filter_text={filter_text}&strategy={strategy}")
        response = await BaseAuthIRBIS.get_response(link)

        category: Optional[dict] = dict()

        result_response = dict()
        if response is not None:
            for data_response in response:
                result_response[data_response["type"]] = data_response["count"]

        category = result_response
        return category

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
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-judge.json?event=role-data&version=2"
                f"&page={page}&rows={rows}&strategy={strategy}"
                f"&filter0={filter0}&filter_text={filter_text}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_court_cases(irbis_person_id: int, person_uuid: str, match_type: MatchType):
        """Обрабатывает данные судебных дел для указанного типа фильтра."""
        court_gen_full = []
        page = 1
        full_data = ['']

        while full_data:
            full_data = await CourtGeneralJurisdiction.get_full_data(
                person_uuid=person_uuid,
                page=page,
                rows=50,
                filter0=match_type.name,
                filter_text='',
                strategy='all'
            )

            for case_data in full_data:
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

                case = CourtGeneralJurFullTable(
                    irbis_person_id=irbis_person_id,
                    faces=faces,
                    progress=progress,
                    case_number=header_data.get("case_number"),
                    region=header_data.get("region"),
                    court_name=header_data.get("court_name"),
                    process_type=header_data.get("process_type"),
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
            page += 1

        return court_gen_full
