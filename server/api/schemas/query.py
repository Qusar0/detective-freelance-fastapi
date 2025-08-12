from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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


class QueryDataRequest(BaseModel):
    query_id: int
    keyword_type_category: str
    page: int = 1
    size: int = 10


class QueryDataResult(BaseModel):
    title: Optional[str]
    info: Optional[str]
    url: Optional[str]
    publication_date: Optional[str]
    keyword_type_name: Optional[str]
    resource_type: Optional[str]


class QueryDataResponse(BaseModel):
    data: List[QueryDataResult]
    total: int
    page: int
    size: int
    total_pages: int


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


class LanguageResponse(BaseModel):
    code: str
    name: str


class CategoryResponse(BaseModel):
    code: str
    name: str


class GenerarQueryDataResponse(BaseModel):
    query_id: int
    query_title: str
    languages: List[LanguageResponse]
    categories: List[CategoryResponse]
    plus_words: List[str]
    minus_words: List[str]
    keyword_stats: Dict[str, int]
    free_words: Optional[List[str]]

    class Config:
        json_schema_extra = {
            "example": {
                "query_id": 123,
                "query_title": "Поиск новостей о компании",
                "languages": [
                    {"code": "ru", "name": "Русский"},
                    {"code": "en", "name": "Английский"}
                ],
                "categories": [
                    {"code": "reputation", "name": "Репутация"},
                    {"code": "negativ", "name": "Негатив"}
                ],
                "plus_words": ["качество", "сервис"],
                "minus_words": ["брак", "возврат"],
                "keyword_stats": {
                    "reputation": 15,
                    "negativ": 8,
                    "free word": 3
                },
                "free_words": ["инновации", "развитие", "технологии"]
            }
        }
