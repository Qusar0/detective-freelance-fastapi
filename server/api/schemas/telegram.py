from pydantic import BaseModel, Field


class WriteSupportRequest(BaseModel):
    theme: str = Field(..., example="Проблема с оплатой")
    description: str = Field(..., example="Не пришли деньги")
    contacts: str = Field(..., example="telegram: @username")


class WriteSupportResponse(BaseModel):
    status: str = Field(..., example="message sent.")
