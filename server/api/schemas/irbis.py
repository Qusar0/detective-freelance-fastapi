from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field
from datetime import datetime


class MatchTypeInfo(BaseModel):
    id: int = Field(..., description="ID типа совпадения")
    name: str = Field(..., description="Название типа совпадения")


class CourtGeneralFace(BaseModel):
    role: str = Field(..., description="Роль лица в деле")
    face: str = Field(..., description="ФИО лица")
    role_name: str = Field(..., description="Название роли на русском языке")


class CourtGeneralProgress(BaseModel):
    name: str = Field(..., description="Название этапа процесса")
    progress_data: str = Field(..., description="Дата этапа процесса")
    resolution: Optional[str] = Field(None, description="Решение по этапу")


class RegionInfo(BaseModel):
    code: int = Field(..., description="Код региона (субъекта РФ)")
    name: str = Field(..., description="Название региона")


class ProcessTypeInfo(BaseModel):
    code: str = Field(..., description="Код типа процесса (A, G, U, M, O)")
    name: str = Field(..., description="Название типа процесса")


class CourtGeneralCase(BaseModel):
    case_id: int = Field(..., description="ID дела в базе данных")
    case_number: str = Field(..., description="Номер дела")
    court_name: str = Field(..., description="Название суда")
    start_date: str = Field(..., description="Дата начала дела")
    end_date: str = Field(..., description="Дата окончания дела (или 'to date' если еще продолжается)")
    review: int = Field(..., description="Количество аппеляций")
    region: RegionInfo = Field(..., description="Информация о регионе")
    process_type: ProcessTypeInfo = Field(..., description="Информация о типе процесса")
    judge: Optional[str] = Field(None, description="ФИО судьи")
    papers: str = Field(..., description="Категория дела из первоисточника")
    papers_pretty: str = Field(..., description="Категория дела (эталонная)")

    @validator('start_date', 'end_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')  # Только дата
            except (ValueError, AttributeError):
                return value
        return value


class IrbisDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")

    all_regions: bool = Field(True, description="True - все регионы, False - только выбранные регионы")

    case_categories: Optional[List[str]] = Field(
        None,
        description="Список категорий дел (коды: A, G, U, M, O). Если None - все категории",
    )


class IrbisPersonInfo(BaseModel):
    fullname: str = Field(..., description="Полное ФИО человека")
    birth_date: Optional[str] = Field(None, description="Дата рождения в формате ДД.ММ.ГГГГ")
    passport_series: Optional[str] = Field(None, description="Серия паспорта")
    passport_number: Optional[str] = Field(None, description="Номер паспорта")
    inn: Optional[str] = Field(None, description="ИНН")
    regions: List[RegionInfo] = Field(..., description="Список выбранных регионов для поиска")


class CourtGeneralCaseFull(BaseModel):
    case_id: int = Field(..., description="ID дела в базе данных")
    case_number: str = Field(..., description="Номер дела")
    court_name: str = Field(..., description="Название суда")
    start_date: str = Field(..., description="Дата начала дела")
    end_date: str = Field(..., description="Дата окончания дела")
    review: Optional[int] = Field(None, description="Количество аппеляций")
    judge: Optional[str] = Field(None, description="ФИО судьи")
    articles: Optional[List[str]] = Field(None, description="Статьи закона")
    papers: Optional[str] = Field(None, description="Категории дела из первоисточника")
    papers_pretty: Optional[str] = Field(None, description="Категории дела (эталонные)")
    links: Optional[Dict[str, List[str]]] = Field(None, description="Ссылки на документы")

    region: RegionInfo = Field(..., description="Информация о регионе")
    process_type: ProcessTypeInfo = Field(..., description="Информация о типе процесса")
    match_type: Optional[MatchTypeInfo] = Field(None, description="Информация о типе совпадения")

    faces: List[CourtGeneralFace] = Field(..., description="Участники дела")
    progress: List[CourtGeneralProgress] = Field(..., description="Ход процесса")
