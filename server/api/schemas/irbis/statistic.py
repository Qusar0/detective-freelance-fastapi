from typing import Optional
from pydantic import BaseModel, Field


class StatisticGeneralCase(BaseModel):
    arbitration_court: Optional[int] = Field(..., description="Количество записей об арбитражных судах")
    bankruptcy: Optional[int] = Field(..., description="Количество записей о банкротстве")
    corruption: Optional[int] = Field(..., description="Количество записей о коррупции")
    court_general: Optional[int] = Field(..., description="Количество записей из судов общей юрисдикции")
    disqualified_person: Optional[int] = Field(..., description="Количество записей о дисквалификации")
    pledgess: Optional[int] = Field(..., description="Количество записей о залогах")
