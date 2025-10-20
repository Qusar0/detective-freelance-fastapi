from typing import Optional, List
from pydantic import BaseModel, validator, Field
from datetime import datetime


class BankruptcyDataCase(BaseModel):
    id: int = Field(..., description="ID дела в базе данных")
    first_name: Optional[str] = Field(..., description="Имя")
    second_name: Optional[str] = Field(..., description="Фамилия")
    last_name: Optional[str] = Field(..., description="Отчество")
    category_name: Optional[str] = Field(..., description="Категория дела")
    birth_date: Optional[str] = Field(..., description="Дата рождения")
    born_place: Optional[str] = Field(..., description="Место рождения")
    region_name: Optional[str] = Field(..., description="Регион")

    @validator('birth_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return value
        return value


class BankruptcyDataResponse(BaseModel):
    cases: List[BankruptcyDataCase] = Field(..., description="Список дел для текущей страницы")
    total_count: int = Field(..., description="Общее количество дел с учетом фильтров")
    total_pages: int = Field(..., description="Общее количество страниц для пагинации")


class BankruptcyDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")

    search_type: Optional[str] = Field(..., description="Тип поиска(name или inn)")


class BankruptcyCaseFull(BaseModel):
    id: int = Field(..., description="ID дела в базе данных")
    first_name: Optional[str] = Field(..., description="Имя")
    second_name: Optional[str] = Field(..., description="Отчество")
    last_name: Optional[str] = Field(..., description="Фамилия")
    birth_date: Optional[str] = Field(..., description="Дата рождения")
    born_place: Optional[str] = Field(..., description="Место рождения")
    inn: Optional[str] = Field(..., description="ИНН")
    ogrn: Optional[str] = Field(..., description="ОГРН")
    snils: Optional[str] = Field(..., description="СНИЛС")
    old_name: Optional[str] = Field(None, description="Прежнее имя")
    category_name: Optional[str] = Field(..., description="Название категории")
    location: Optional[str] = Field(..., description="Местоположение")
    region_name: Optional[str] = Field(..., description="Название региона")
    information: Optional[str] = Field(..., description="Дополнительная информация")
    link: Optional[str] = Field(..., description="Ссылки")
