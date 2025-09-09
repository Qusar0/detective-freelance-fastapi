from pydantic import BaseModel, Field
from typing import List, Optional, Dict


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
    search_plus: str = Field(..., description="Строка содержащая список плюс слов", example="+кот+собака")
    search_minus: str = Field(..., description="Строка содержащая список минус слов", example="+-кот+-собака")
    keywords: List[str] = Field(..., description="Список ключевых слов")
    default_keywords_type: str = Field(
        ...,
        description="Типы поиска по ключевым словам",
        example="negativ, reputation",
    )
    search_engines: List[str] = Field(
        ...,
        description="Список поисковых систем для поиска",
        example=["google", "yandex"],
    )
    languages: List[str] = Field(
        ...,
        description="Список языков перевода данных",
        example=["en", "es"],
    )


class FindByNumberModel(BaseModel):
    search_number: str = Field(..., description="Номер телефона в международном формате")
    methods_type: List[str] = Field(..., description="Список методов поиска", example=["mentions"])


class FindByEmailModel(BaseModel):
    email: str = Field(..., description="Email человека")
    methods_type: List[str] = Field(
        ...,
        description="Список методов поиска",
        example=["mentions"],
    )


class FindByCompanyModel(BaseModel):
    company_name: str = Field(..., description="Название организации")
    extra_name: Optional[str] = Field(description="Дополнительное название организации")
    location: Optional[str] = Field(description="Расположение организации")
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    default_keywords_type: str = Field(
        ...,
        description="Типы поиска по ключевым словам",
        example="company_negativ, company_reputation",
    )
    search_plus: str = Field(..., description="Строка содержащая список плюс слов", example="+кот+собака")
    search_minus: str = Field(..., description="Строка содержащая список минус слов", example="+-кот+-собака")
    search_engines: List[str] = Field(
        ...,
        description="Список поисковых систем для поиска",
        example=["google", "yandex"],
    )
    languages: List[str] = Field(..., description="Список языков перевода данных", example=["en", "es"])


class CalculatePriceRequest(BaseModel):
    search_patronymic: str = Field(..., description="Отчество искомого")
    keywords: List[str] = Field(..., description="Список ключевых слов")
    default_keywords_type: str = Field(
        ...,
        description="Типы поиска по ключевым словам",
        example="negativ, reputation",
    )
    languages: List[str] = Field(..., description="Список языков перевода данных", example=["en", "es"])


class PriceResponse(BaseModel):
    price: float = Field(..., description="Цена выполнения запроса")


class DownloadQueryRequest(BaseModel):
    query_id: int = Field(..., description="ID запроса в БД")


class FindByIRBISModel(BaseModel):
    first_name: str = Field(..., description="Имя человека")
    last_name: str = Field(..., description="Фамилия человека")
    regions: list[int] = Field(
        ...,
        description="Список регионов. Максимум значений - 2",
        example=[77, 69],
    )
    second_name: Optional[str] = Field(description="Отчество человека")
    birth_date: Optional[str] = Field(description="Дата рождения человека")
    passport_series: Optional[str] = Field(description="Серия паспорта человека")
    passport_number: Optional[str] = Field(description="Номер паспорта человека")
    inn: Optional[str] = Field(description="ИНН человека")


class QueryDataRequest(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    keyword_type_category: str = Field(..., description="Тип поиска по категориям", example='socials')
    page: int = Field(1, description="Номер страницы")
    size: int = Field(20, description="Количество записей на странице")


class CategoryQueryDataRequest(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    keyword_type_category: str = Field(..., description="Тип поиска по категориям", example='socials')
    size: int = Field(20, description="Количество записей")


class QueryDataResult(BaseModel):
    title: Optional[str] = Field(description="Название источника")
    info: Optional[str] = Field(description="Информация из источника")
    url: Optional[str] = Field(description="Ссылка на источник источника")
    publication_date: Optional[str] = Field(description="Дата публикации источника")
    keyword_type_name: Optional[str] = Field(description="Тип категории")
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    resource_type: Optional[str] = Field(description="Тип источника информации")


class NameQueryDataResult(BaseModel):
    title: Optional[str] = Field(description="Название источника")
    info: Optional[str] = Field(description="Информация из источника")
    url: Optional[str] = Field(description="Ссылка на источник источника")
    publication_date: Optional[str] = Field(description="Дата публикации источника")
    keyword_type_name: Optional[str] = Field(description="Тип категории")
    keywords: Optional[List[str]] = Field(description="Список ключевых слов")
    resource_type: Optional[str] = Field(description="Тип источника информации")
    is_fullname: bool = Field(description="Является ли ФИО")


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
    title: str = Field(..., description="Найденное название")
    snippet: str = Field(..., description="Сниппет")
    url: str = Field(..., description="Ссылка на источник")
    publication_date: Optional[str] = Field(..., description="Дата публикации")
    uri: str = Field(..., description="Uri источника")
    weight: int = Field(
        1,
        description="Вес материала (зависит от количества совпадений материала по нескольким ключевым словам)",
    )
    kwd: str = Field(..., description="Ключевое слово")
    word_type: Optional[str] = Field(None, description="Тип ключевого слова")
    kwds_list: List[str] = Field(
        description="Список ключевых слов",
        default_factory=list,
    )
    fullname: str = Field("false", description="Является ли ФИО")
    soc_type: Optional[str] = Field(None, description="Тип социальной сети")
    doc_type: str = Field("", description="Тип документа")


class NumberInfo(BaseModel):
    """Модель для хранения информации о найденных номерах"""
    title: str = Field(..., description="Найденное название")
    snippet: str = Field(..., description="Сниппет")
    url: str = Field(..., description="Ссылка на источник")
    uri: str = Field(..., description="Uri источника")
    weight: int = Field(
        1,
        description="Вес материала (зависит от количества совпадений материала по нескольким ключевым словам)",
    )
    kwd: str = Field(..., description="Ключевое слово")


class LanguageResponse(BaseModel):
    code: str = Field(..., description="Код языка")
    name: str = Field(..., description="Название языка")


class CategoryResponse(BaseModel):
    code: str = Field(..., description="Код поиска на английском языке")
    name: str = Field(..., description="Название типа поиска")


class GenerarQueryDataResponse(BaseModel):
    query_id: int = Field(..., description="Id запроса")
    query_title: str = Field(..., description="Название запроса")
    languages: List[LanguageResponse] = Field(..., description="Список языков перевода")
    categories: List[CategoryResponse] = Field(..., description="Список категорий поиска")
    plus_words: List[str] = Field(..., description="Список плюс слов запроса")
    minus_words: List[str] = Field(..., description="Список минус слов запроса")
    keyword_stats: Dict[str, int] = Field(
        ...,
        description="Статистика собранных данных в формате 'тип_поиска: количество результатой'",
    )
    free_words: Optional[List[str]] = Field(..., description="Список ключевых слов от пользователя")
