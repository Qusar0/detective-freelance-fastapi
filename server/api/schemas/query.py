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
    search_engines: List[str]
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
    search_engines: List[str]
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


class FindByIRBISModel(BaseModel):
    first_name: str
    last_name: str
    regions: list[int]
    second_name: Optional[str]
    birth_date: Optional[str]
    passport_series: Optional[str]
    passport_number: Optional[str]
    inn: Optional[str]


class ShortQueryDataResult(BaseModel):
    """Модель для одного результата запроса"""
    title: Optional[str]
    info: Optional[str]
    url: Optional[str]
    publication_date: Optional[str] = None


class QueryDataResult(BaseModel):
    """Модель для одного результата запроса"""
    title: Optional[str]
    info: Optional[str]
    url: Optional[str]
    publication_date: Optional[str] = None
    keyword_type: str
    resource_type: Optional[str] = None


class FoundInfo(BaseModel):
    """Модель для хранения информации о найденных результатах"""
    title: str
    snippet: str
    url: str
    publication_date: Optional[str]
    uri: str
    weight: int = 1
    kwd: str
    word_type: Optional[str] = None
    kwds_list: List[str] = Field(default_factory=list)
    fullname: str = "false"
    soc_type: Optional[str] = None
    doc_type: str = ""


class NumberInfo(BaseModel):
    """Модель для хранения информации о найденных номерах"""
    title: str
    snippet: str
    url: str
    uri: str
    weight: int = 1
    kwd: str
