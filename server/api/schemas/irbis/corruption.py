from typing import Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class CorruptionDataCase(BaseModel):
    """Краткая информация о деле (список)."""
    id: int = Field(..., description="ID записи в базе данных")
    full_name: str = Field(..., description="ФИО")
    organization: str = Field(..., description="Организация")
    position: str = Field(..., description="Должность")
    application_date: Optional[str] = Field(None, description="Дата подачи")

    @validator("application_date", pre=True)
    def parse_application_date(cls, value):
        if not value:
            return value
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                return value
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return value


class CorruptionDataRequest(BaseModel):
    """Параметры запроса списка с пагинацией."""
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")


class CorruptionCaseFull(BaseModel):
    """Полная информация о деле."""
    id: int = Field(..., description="ID записи")
    full_name: str = Field(..., description="ФИО")
    organization: Optional[str] = Field(None, description="Организация")
    position: Optional[str] = Field(None, description="Должность")
    normative_act: Optional[str] = Field(None, description="Нормативный акт")
    application_date: Optional[str] = Field(None, description="Дата подачи")
    publish_date: Optional[str] = Field(None, description="Дата публикации")
    excluded_reason: Optional[str] = Field(None, description="Причина исключения")

    @validator("application_date", "publish_date", pre=True)
    def parse_dates(cls, value):
        if not value:
            return value
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                return value
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return value
