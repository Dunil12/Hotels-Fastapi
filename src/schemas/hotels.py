from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str | None
    name: str | None

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)


