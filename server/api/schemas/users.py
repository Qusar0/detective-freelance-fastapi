from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    stay_logged_in: Optional[bool] = Field(default=False)


class AuthResponse(BaseModel):
    message: str
    user_id: int
    email: EmailStr
    created: str


class StatusMessage(BaseModel):
    status: str
    message: str


class AuthStatusResponse(BaseModel):
    status: str
    message: str


class TopUpBalanceResponseData(BaseModel):
    new_balance: float = Field(..., description="Новый баланс пользователя")
    transaction_id: str = Field(..., description="ID транзакции")
    amount: float = Field(..., description="Сумма пополнения")
    currency: str = Field(..., description="Валюта")
    operation_date: datetime = Field(..., description="Дата и время операции")
    invoice_id: Optional[str] = Field(None, description="ID счета (если есть)")


class TopUpBalanceResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="Баланс успешно пополнен")
    data: TopUpBalanceResponseData


class TopUpBalanceQueryParams(BaseModel):
    transaction_id: int = Field(..., description="Идентификатор транзакции")
    currency: str = Field(..., description="Валюта платежа")
    payment_amount: float = Field(..., description="Сумма платежа")
    operation_type: str = Field(..., description="Тип операции")
    invoice_id: Optional[int] = Field(None, description="Идентификатор счёта")
    account_id: int = Field(..., description="ID аккаунта пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    date_time: datetime = Field(..., description="Дата и время операции в ISO-формате")
    ip_address: Optional[str] = Field(None, description="IP-адрес пользователя")
    status: str = Field(..., description="Статус транзакции")


class ConfirmResponse(BaseModel):
    status: str
    message: str


class ChangeEventStatusRequest(BaseModel):
    event_id: int = Field(..., description="ID события")


class ChangePasswordRequest(BaseModel):
    old_password: constr(min_length=8) = Field(..., description="Старый пароль (минимум 8 символов)")
    new_password: constr(min_length=8) = Field(..., description="Новый пароль (минимум 8 символов)")


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class SetDefaultLanguageRequest(BaseModel):
    default_language_id: int = Field(..., description="ID языка по умолчанию из таблицы languages")


class SetDefaultLanguageResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="Язык по умолчанию обновлен")
    default_language_id: int = Field(..., description="ID текущего языка по умолчанию")


class GetDefaultLanguageResponse(BaseModel):
    status: str = Field(..., example="success")
    default_language_id: int = Field(..., description="ID языка по умолчанию пользователя")
