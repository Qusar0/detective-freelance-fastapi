from typing import List, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class PledgessGeneralPledgees(BaseModel):  # таблица pledge_parties
    name: str = Field(..., description="Название заемщика/Занимателя")


class PledgessGeneralPledges(BaseModel):  # таблица pledge_items
    pledge_type: str = Field(..., description="Тип залога")
    pledge_num: str = Field(..., description="Номер залога")


class PledgessGeneralCase(BaseModel):
    case_id: int = Field(..., description="ID дела в базе данных")
    pledge_type: str = Field(..., description="Тип залога")
    reg_date: str = Field(..., description="Дата регистрации")

    pledgers: List[PledgessGeneralPledgees] = Field(..., description="Заемщики")
    pledgees: List[PledgessGeneralPledgees] = Field(..., description="Организации")
    pledges: List[PledgessGeneralPledges] = Field(..., description="Предметы залога")

    @validator('reg_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return value
        return value


class PledgessDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")


class PledgePartiesSchema(BaseModel):
    name: str = Field(..., description="Наименование стороны (физическое или юридическое лицо)")
    birth_date: Optional[str] = Field(None, description="Дата рождения (для физических лиц)")
    inn: Optional[str] = Field(None, description="ИНН стороны")
    ogrn: Optional[str] = Field(None, description="ОГРН/ОГРНИП (для юридических лиц и ИП)")


class PledgeObjectSchema(BaseModel):
    pledge_num_name: str = Field(..., description="Наименование номера записи о залоге")
    pledge_num: str = Field(..., description="Номер записи о залоге")
    pledge_type: str = Field(..., description="Тип предмета залога (недвижимость, транспорт и т.д.)")


class PledgessCaseFull(BaseModel):
    case_id: int = Field(..., description="Уникальный идентификатор дела о залоге в базе данных")
    reg_date: str = Field(..., description="Дата регистрации дела о залоге")
    pledge_reestr_number: str = Field(..., description="Реестровый номер записи о залоге")
    pledge_type: str = Field(..., description="Тип залогового дела")

    pledgers: List[PledgePartiesSchema] = Field(..., description="Заемщики")
    pledgees: List[PledgePartiesSchema] = Field(..., description="Организации")
    pledges: List[PledgeObjectSchema] = Field(..., description="Список предметов залога по делу")
