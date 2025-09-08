from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class DeleteQueryRequest(BaseModel):
    query_id: int = Field(..., description="ID запроса", example="975")


class ErrorResponse(BaseModel):
    status: str = Field(..., description="Код ошибки", example="error")
    message: str = Field(..., description="Сообщение ошибки", example="Some error message")


class SuccessResponse(BaseModel):
    message: str = Field(..., description="Сообщение об успехе", example="Success")


class QueriesCountResponse(BaseModel):
    count: int = Field(..., description="Количество ответов в 1 запросе", example=5)


class QueryData(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    query_title: str = Field(..., description="Название запроса")
    query_created_at: str = Field(..., description="Дата создания запроса")
    query_status: str = Field(..., description="Статус запроса")
    balance: float = Field(..., description="Баланс запроса")


class FindByNameModel(BaseModel):
    search_name: str = Field(..., description="Имя искомого")
    search_surname: str = Field(..., description="Фамилия искомого")
    search_patronymic: str = Field(..., description="Отчество искомого")
    search_plus: str
    search_minus: str
    keywords: List[str] = Field(..., description="Список ключевых слов")
    default_keywords_type: str
    search_engines: List[str]
    languages: List[str] = Field(..., description="Список языков перевода данных", example=["en", "es"])


class SearchResponseModel(BaseModel):
    query_id: int
    query_title: str
    query_status: str
    query_created_at: datetime
    balance: float


class FindByNumberModel(BaseModel):
    search_number: str = Field(..., description="Номер телефона человека, которго необходимо найти")
    methods_type: List[str] = Field(..., description="Список методов поиска человека по телефону",
                                    example=["mentions"])


class FindByEmailModel(BaseModel):
    email: str = Field(..., description="Email человека, которго необходимо найти")
    methods_type: List[str] = Field(..., description="Список методов поиска человека по email",
                                    example=["mentions", "acc checker"])


class FindByCompanyModel(BaseModel):
    company_name: str = Field(..., description="Название организации")
    extra_name: Optional[str] = Field(description="Дополнительное название организации")
    location: Optional[str] = Field(description="Расположение организации")
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    default_keywords_type: Optional[str]
    search_plus: Optional[str]
    search_minus: Optional[str]
    search_engines: List[str]
    languages: List[str] = Field(..., description="Список языков перевода данных", example=["en", "es"])


class CalculatePriceRequest(BaseModel):
    search_patronymic: str = Field(..., description="Отчество искомого")
    keywords: List[str] = Field(..., description="Список ключевых слов")
    default_keywords_type: str
    languages: List[str] = Field(..., description="Список языков перевода данных", example=["en", "es"])


class PriceResponse(BaseModel):
    price: float = Field(..., description="Цена выполнения запроса")


class DownloadQueryRequest(BaseModel):
    query_id: int = Field(..., description="ID запроса в БД")


class FindByIRBISModel(BaseModel):
    first_name: str = Field(..., description="Имя человека, которого необходимо найти")
    last_name: str = Field(..., description="Фамилия человека, которого необходимо найти")
    regions: list[int] = Field(..., description="Список регионов, по которым необходимо искать человека. "
                                                        "Максимум значений - 2")
    second_name: Optional[str] = Field(description="Отчество человека, которого необходимо найти")
    birth_date: Optional[str] = Field(description="Дата рождения человека, которого необходимо найти")
    passport_series: Optional[str] = Field(description="Серия паспорта человека,"
                                                                     " которго необходимо найти")
    passport_number: Optional[str] = Field(description="Номер паспорта человека,"
                                                                     " которго необходимо найти")
    inn: Optional[str] = Field(description="ИНН человека, которого необходимо найти")


class QueryDataRequest(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    keyword_type_category: str
    page: int = Field(1, description="Номер страницы")
    size: int = Field(20, description="Количество записей на странице")


class CategoryQueryDataRequest(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    keyword_type_category: str
    size: int = Field(20, description="Количество записей")


class QueryDataResult(BaseModel):
    title: Optional[str] = Field(description="Название источника")
    info: Optional[str] = Field(description="Информация из источника")
    url: Optional[str] = Field(description="Ссылка на источник источника")
    publication_date: Optional[str] = Field(description="Дата публикации источника")
    keyword_type_name: Optional[str]
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    resource_type: Optional[str] = Field(description="Тип источника информации")


class NameQueryDataResult(BaseModel):
    title: Optional[str] = Field(description="Название источника")
    info: Optional[str] = Field(description="Информация из источника")
    url: Optional[str] = Field(description="Ссылка на источник источника")
    publication_date: Optional[str] = Field(description="Дата публикации источника")
    keyword_type_name: Optional[str]
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    resource_type: Optional[str] = Field(description="Тип источника информации")
    is_fullname: bool = Field(description="Полное имя")


class QueryDataResponse(BaseModel):
    total: int = Field(..., description="Количество информации по категории")
    size: int = Field(..., description="Количество запрашиваемой информации")
    total_pages: int = Field(..., description="Количество страниц")


class NameQueryDataResponse(BaseModel):
    total: int = Field(..., description="Количество информации по категории")
    fullname_count: int = Field(..., description="Количество записей с полным именем")
    size: int = Field(..., description="Количество запрашиваемой информации")
    total_pages: int = Field(..., description="Количество страниц")


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
    code: str = Field(..., description="Код языка")
    name: str = Field(..., description="Название языка")


class CategoryResponse(BaseModel):
    code: str
    name: str


class GenerarQueryDataResponse(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    query_title: str = Field(..., description="Название запроса")
    languages: List[LanguageResponse] = Field(..., description="Список языков перевода")
    categories: List[CategoryResponse] = Field(..., description="Список категорий поиска")
    plus_words: List[str]
    minus_words: List[str]
    keyword_stats: Dict[str, int]
    free_words: Optional[List[str]]
