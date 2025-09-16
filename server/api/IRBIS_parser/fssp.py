from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import FSSPFullTable

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
    
    @staticmethod
    async def _process_fssp_data(irbis_person_id: int, person_uuid: str):
        """Обработка данных ФССП с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await FSSP.get_full_data(person_uuid, page, 50)
            if not data:
                break
            full_data.extend(data)
            page += 1

        return [
            FSSPFullTable(
                irbis_person_id=irbis_person_id,
                ip=item.get("ip"),
                fio=item.get("fio"),
                rosp=item.get("rosp"),
                type_ip=item.get("type_ip"),
                summ=item.get("summ"),
                rekv=item.get("rekv"),
                end_cause=item.get("end_cause"),
                pristav=item.get("pristav"),
                pristav_phones=item.get("pristav_phones")
            )
            for item in full_data
        ]
