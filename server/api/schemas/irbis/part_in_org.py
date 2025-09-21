from typing import List, Optional
from pydantic import BaseModel, Field


class PartInOrgGeneralCase(BaseModel):
    case_id: int = Field(..., description="Уникальный идентификатор дела в системе")
    individual_name: Optional[str] = Field(None, description="ФИО физического лица, участвующего в деле")
    org_name: Optional[str] = Field(None, description="Наименование организации, участвующей в деле")
    org_okved: Optional[str] = Field(None, description="Код ОКВЭД организации (основной вид деятельности)")


class PartInOrgDataRequest(BaseModel):
    query_id: int = Field(..., description="Идентификатор запроса для отслеживания")
    page: int = Field(1, ge=1, description="Номер страницы для пагинации (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество результатов на странице (от 1 до 100)")


class OrgObjectSchema(BaseModel):
    name: str = Field(..., description="Полное наименование юридического лица")
    inn: Optional[str] = Field(None, description="ИНН организации")
    ogrn: Optional[str] = Field(None, description="ОГРН юридического лица")
    address: Optional[str] = Field(None, description="Юридический адрес организации")
    okved: Optional[str] = Field(None, description="Код ОКВЭД основного вида деятельности")


class RoleObjectSchema(BaseModel):
    name: str = Field(..., description="Наименование роли/должности в организации")
    active: bool = Field(..., description="Статус активности роли (true - активна, false - неактивна)")


class IndividualObjectSchema(BaseModel):
    name: str = Field(..., description="Полное ФИО физического лица")
    inn: str = Field(..., description="ИНН физического лица")
    roles: List[RoleObjectSchema] = Field(..., description="Список ролей и должностей лица в организациях")


class PartInOrgCaseFull(BaseModel):
    case_id: int = Field(..., description="Уникальный идентификатор дела")

    org_data: Optional[OrgObjectSchema] = Field(None, description="Данные об организации-участнике дела")
    individual: Optional[IndividualObjectSchema] = Field(None, description="Данные физлица-участника дела")
