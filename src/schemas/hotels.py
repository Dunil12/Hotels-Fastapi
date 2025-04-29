from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str | None
    location: str | None

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
