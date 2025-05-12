from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str | None
    location: str | None

class Hotel(HotelAdd):
    id: int | None

class HotelPatch(BaseModel):
    title: str
    location: str
    # location: str | None = Field(None)
