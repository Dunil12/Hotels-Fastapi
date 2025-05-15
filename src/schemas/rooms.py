from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    price: int
    description:str | None = None
    quantity: int

class RoomPatch(BaseModel):
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int

class Room(RoomAdd):
    id: int
