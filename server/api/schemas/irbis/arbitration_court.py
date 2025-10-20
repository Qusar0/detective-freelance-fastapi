from typing import List, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime
from server.api.schemas.irbis.irbis_general import RoleTypeInfo


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
        description="Роль человека в деле. Если None - все роли",
    )


class CaseTypeInfo(BaseModel):
    id: int = Field(..., description="ID типа дела")
    name: str = Field(..., description="Название типа дела")


class ArbitrationCourtCase(BaseModel):
    id: int = Field(..., description="ID дела в базе данных")
    court_name: Optional[str] = Field(..., description="Название суда")
    case_date: Optional[str] = Field(..., description="Дата дела")
    name: Optional[str] = Field(..., description="ФИО участника дела")
    case_number: Optional[str] = Field(..., description="Номер дела")
    address: Optional[str] = Field(..., description="Адрес")
    search_type: Optional[str] = Field(..., description="Тип поиска")

    inn: Optional[str] = Field(None, description="ИНН")
    case_type: Optional[CaseTypeInfo] = Field(None, description="Тип дела")
    role: Optional[RoleTypeInfo] = Field(None, description="Роль в деле")

    @validator('case_date', pre=True)
    def parse_date(cls, value):
        """Парсит дату в единый формат"""
        if isinstance(value, str):
            try:
                if 'T' in value and 'Z' in value:
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d')
                else:
                    dt = datetime.strptime(value, '%Y-%m-%d')
                    return dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return value
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%d')
        return value


class ArbitrationCourtDataResponse(BaseModel):
    cases: List[ArbitrationCourtCase] = Field(..., description="Список дел для текущей страницы")
    total_count: int = Field(0, description="Общее количество дел с учетом фильтров")
    total_pages: int = Field(0, description="Общее количество страниц для пагинации")


class ArbitrationCourtCaseFull(BaseModel):
    id: int = Field(..., description="ID дела в базе данных")
    court_name: Optional[str] = Field(..., description="Название суда")
    case_date: Optional[str] = Field(..., description="Дата дела")
    name: Optional[str] = Field(..., description="ФИО участника дела")
    case_number: Optional[str] = Field(..., description="Номер дела")
    address: Optional[str] = Field(..., description="Адрес")

    inn: Optional[str] = Field(None, description="ИНН")
    case_type: Optional[str] = Field(None, description="Тип дела")
    role: Optional[str] = Field(None, description="Роль в деле")
    region: Optional[str] = Field(None, description="Информация о регионе")
    opponents: List[str] = Field(..., description="Опоненты дела")
