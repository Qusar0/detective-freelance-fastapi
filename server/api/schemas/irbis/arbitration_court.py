from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Field
from datetime import datetime
from server.api.schemas.irbis.irbis_general import (
    RegionInfo,
    ProcessTypeInfo,
    MatchTypeInfo,
)


class ArbitrationCourtDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")

    search_type: Optional[str] = Field(
        None,
        description="name - По инициалам ФИО, inn - По ИНН. Если None - все записи",
    )

    role: Optional[str] = Field(
        None,
        description="Роль человека в деле (коды: P, R). Если None - все роли",
    )


class ArbitrationCourtCase(BaseModel):
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
