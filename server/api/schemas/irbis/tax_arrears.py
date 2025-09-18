from typing import List
from decimal import Decimal
from pydantic import BaseModel, Field


class InfoItemCase(BaseModel):
    value: str = Field(..., description="Причина задолженности")


class PaymentItemCase(BaseModel):
    name: str = Field(..., description="Наименование получателя")
    value: str = Field(..., description="Адрес получателя")


class TaxArrearsDataCase(BaseModel):
    provider: str = Field(..., description="Провайдер")
    money_name: str = Field(..., description="Валюта")
    value: Decimal = Field(..., description="Сумма задолженности")
    info: List[InfoItemCase] = Field(None, description="Информация о задолженностях")
    payment: List[PaymentItemCase] = Field(None, description="Информация о реквизитах")


class TaxArrearsDataRequest(BaseModel):
    """Параметры запроса списка с пагинацией."""
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")