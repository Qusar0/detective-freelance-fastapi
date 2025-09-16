from typing import Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class FSSPDataCase(BaseModel):
    """Краткая информация о деле (список)."""
    id: int = Field(..., description="ID записи в базе данных")
    fio: str = Field(..., description="ФИО")
    type_ip: str = Field(..., description="Тип испольнительного производства")
    summ: float = Field(..., description="Сумма")
    end_cause: Optional[str] = Field(None, description="Конечная причина")


class FSSPDataRequest(BaseModel):
    """Параметры запроса списка с пагинацией."""
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")


class FSSPCaseFull(BaseModel):
    """Полная информация о деле."""
    id: int = Field(..., description="ID записи")
    ip: str = Field(..., description="Испольнительное производство")
    fio: str = Field(..., description="ФИО")
    rosp: str = Field(..., description="Районный отдел судебных приставов")
    type_ip: str = Field(..., description="Тип испольнительного производства")
    summ: float = Field(..., description="Сумма")
    rekv: str = Field(..., description="Реквизиты")
    end_cause: str = Field(..., description="Конечная причина")
    pristav: str = Field(..., description="Пристав")
    pristav_phones: Optional[str] = Field(..., description="Телефон приставов")
