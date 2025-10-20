from typing import Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class DisqDataCase(BaseModel):
    id: int = Field(..., description="ID дела в базе данных")
    fio: Optional[str] = Field(..., description="Фамилия Имя Отчество")
    start_date_disq: Optional[str] = Field(..., description="Дата начала")
    end_date_disq: Optional[str] = Field(..., description="Дата конца")
    article: Optional[str] = Field(..., description="")
    legal_name: Optional[str] = Field(..., description="Настоящее имя")
    office: Optional[str] = Field(..., description="Офис")

    @validator('start_date_disq', 'end_date_disq', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return value
        return value


class DisqDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")


class DisqCaseFull(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор дела в базе данных")
    birth_date: Optional[str] = Field(..., description="Дата рождения лица")
    fio: Optional[str] = Field(..., description="Фамилия, имя, отчество лица")
    article: Optional[str] = Field(..., description="Статья закона, по которой применена дисквалификация")
    start_date_disq: Optional[str] = Field(..., description="Дата начала срока дисквалификации")
    end_date_disq: Optional[str] = Field(..., description="Дата окончания срока дисквалификации")
    bornplace: Optional[str] = Field(..., description="Место рождения лица")
    fio_judge: Optional[str] = Field(..., description="Фамилия, имя, отчество судьи")
    office_judge: Optional[str] = Field(..., description="Должность судьи")
    legal_name: Optional[str] = Field(None, description="Прежнее юридическое название организации")
    office: Optional[str] = Field(..., description="Наименование суда или органа,")
    department: Optional[str] = Field(..., description="Отдел суда")
