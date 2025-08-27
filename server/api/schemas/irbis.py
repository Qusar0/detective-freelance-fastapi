from typing import List, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class CourtGeneralFace(BaseModel):
    role: str
    face: str
    role_name: str


class CourtGeneralProgress(BaseModel):
    name: str
    progress_data: str
    resolution: Optional[str]


class RegionInfo(BaseModel):
    code: int
    name: str


class ProcessTypeInfo(BaseModel):
    code: str
    name: str


class CourtGeneralCase(BaseModel):
    case_id: int
    case_number: str
    court_name: str
    start_date: str
    end_date: str
    review: int
    region: RegionInfo
    process_type: ProcessTypeInfo
    judge: Optional[str] = None
    papers: str
    papers_pretty: str

    @validator('start_date', 'end_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')  # Только дата
            except (ValueError, AttributeError):
                return value
        return value


class IrbisDataRequest(BaseModel):
    query_id: int
    page: int = Field(1, ge=1, description="Номер страницы (начинается с 1)")
    size: int = Field(20, ge=1, le=100, description="Количество элементов на странице (1-100)")

    all_regions: bool = Field(True, description="True - все регионы, False - только выбранные регионы")

    case_categories: Optional[List[str]] = Field(
        None,
        description="Список категорий дел (коды: A, G, U, M, O). Если None - все категории",
    )


class CourtGeneralResponse(BaseModel):
    cases: List[CourtGeneralCase]
