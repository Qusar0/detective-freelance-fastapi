from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DeleteQueryRequest(BaseModel):
    query_id: int = Field(..., example="975")


class ErrorResponse(BaseModel):
    status: str = Field(..., example="error")
    message: str = Field(..., example="Some error message")


class SuccessResponse(BaseModel):
    message: str = Field(..., example="Success")


class QueriesCountResponse(BaseModel):
    count: int = Field(..., example=5)


class QueryData(BaseModel):
    query_id: int
    query_title: str
    query_unix_date: str
    query_created_at: str
    query_status: str
    balance: float


class FindByNameModel(BaseModel):
    search_name: str
    search_surname: str
    search_patronymic: str
    search_plus: str
    search_minus: str
    keywords: List[str]
    default_keywords_type: str
    search_engines: List[str] = Field(example=["goolge", "yandex"])
    languages: List[str] = Field(example=["en", "es"])


class SearchResponseModel(BaseModel):
    query_id: int
    query_title: str
    query_status: str
    query_created_at: datetime
    balance: float


class FindByNumberModel(BaseModel):
    search_number: str
    methods_type: List[str]


class FindByEmailModel(BaseModel):
    email: str
    methods_type: List[str]


class FindByCompanyModel(BaseModel):
    company_name: str
    extra_name: Optional[str]
    location: Optional[str]
    keywords: Optional[List[str]]
    default_keywords_type: Optional[str]
    search_plus: Optional[str]
    search_minus: Optional[str]
    search_engines: List[str] = Field(example=["goolge", "yandex"])
    languages: List[str] = Field(example=["en", "es"])


class CalculatePriceRequest(BaseModel):
    search_patronymic: str
    keywords: List[str]
    default_keywords_type: str
    languages: List[str] = Field(example=["en", "es"])


class PriceResponse(BaseModel):
    price: float


class DownloadQueryRequest(BaseModel):
    query_id: int
