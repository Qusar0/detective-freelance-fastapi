from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class PaymentItemCase(BaseModel):
    name: Optional[str] = Field(..., description="Наименование получателя")
    value: Optional[str] = Field(..., description="Адрес получателя")


class TaxArrearsDataCase(BaseModel):
    provider: Optional[str] = Field(..., description="Провайдер")
    money_name: Optional[str] = Field(..., description="Валюта")
    value: Decimal = Field(..., description="Сумма задолженности")
    info: Optional[List[str]] = Field(default=None, description="Информация о задолженности")
    payment: List[PaymentItemCase] | None = Field(default=None, description="Информация о реквизитах")


class TaxArrearsDataRequest(BaseModel):
    """Параметры запроса списка с пагинацией."""
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")
