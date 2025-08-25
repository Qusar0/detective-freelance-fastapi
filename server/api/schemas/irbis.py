from typing import List, Optional, Dict
from pydantic import BaseModel, validator
from datetime import datetime


class CourtGeneralFace(BaseModel):
    role: str
    face: str
    role_name: str


class CourtGeneralProgress(BaseModel):
    name: str
    progress_data: str
    resolution: Optional[str]


class CourtGeneralCase(BaseModel):
    case_number: str
    court_name: str
    start_date: str  # или datetime если нужно парсить
    end_date: str  # или datetime если нужно парсить
    review: int
    region: int
    process_type: str
    judge: Optional[str] = None
    papers: str
    papers_pretty: str
    links: Dict[str, List[str]]
    progress: List[CourtGeneralProgress]  # или List[Any] если структура неизвестна
    faces: List[CourtGeneralFace]

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
    page: int = 1
    size: int = 10


class CourtGeneralResponse(BaseModel):
    cases: List[CourtGeneralCase]
