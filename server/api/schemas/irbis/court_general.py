from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field
from datetime import datetime
from server.api.schemas.irbis.irbis_general import (
    RegionInfo,
    ProcessTypeInfo,
    MatchTypeInfo,
)


class CourtGeneralFace(BaseModel):
    role: str = Field(..., description="Роль лица в деле")
    face: str = Field(..., description="ФИО лица")
    role_name: str = Field(..., description="Название роли на русском языке")


class CourtGeneralProgress(BaseModel):
    name: str = Field(..., description="Название этапа процесса")
    progress_data: Optional[str] = Field(None, description="Дата этапа процесса")
    resolution: Optional[str] = Field(None, description="Решение по этапу")


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
                return dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return value
        return value


class CourtGeneralDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")

    all_regions: bool = Field(True, description="True - все регионы, False - только выбранные регионы")

    case_categories: Optional[List[str]] = Field(
        None,
        description="Список категорий дел (коды: A, G, U, M, O). Если None - все категории",
    )


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


class CourtGeneralDataResponse(BaseModel):
    cases: List[CourtGeneralCase] = Field(..., description="Список дел для текущей страницы")
    total_count: int = Field(..., description="Общее количество дел с учетом фильтров")
    total_pages: int = Field(..., description="Общее количество страниц для пагинации")
