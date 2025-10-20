from typing import Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class TerroristsDataCase(BaseModel):
    """Краткая информация о деле (список)."""
    id: int = Field(..., description="ID записи в базе данных")
    fio: Optional[str] = Field(..., description="ФИО")
    birth_place: Optional[str] = Field(..., description="Место рождения")
    birth_date: Optional[str] = Field(None, description="Дата рождения")

    @validator("birth_date", pre=True)
    def parse_birth_date(cls, value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                return value.split("T")[0]
        return str(value)


class TerroristsDataRequest(BaseModel):
    """Параметры запроса списка с пагинацией."""
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")
