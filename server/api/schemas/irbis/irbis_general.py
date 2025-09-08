from typing import List, Optional
from pydantic import BaseModel, Field


class MatchTypeInfo(BaseModel):
    id: int = Field(..., description="ID типа совпадения")
    name: str = Field(..., description="Название типа совпадения")


class RegionInfo(BaseModel):
    id: int = Field(..., description="Код региона (субъекта РФ)")
    name: str = Field(..., description="Название региона")


class ProcessTypeInfo(BaseModel):
    code: str = Field(..., description="Код типа процесса")
    name: str = Field(..., description="Название типа процесса")


class RoleTypeInfo(BaseModel):
    id: int = Field(..., description="ID роли участника")
    name: str = Field(..., description="Название роли участника")


class IrbisPersonInfo(BaseModel):
    fullname: str = Field(..., description="Полное ФИО человека")
    birth_date: Optional[str] = Field(None, description="Дата рождения в формате ДД.ММ.ГГГГ")
    passport_series: Optional[str] = Field(None, description="Серия паспорта")
    passport_number: Optional[str] = Field(None, description="Номер паспорта")
    inn: Optional[str] = Field(None, description="ИНН")
    regions: List[RegionInfo] = Field(..., description="Список выбранных регионов для поиска")
