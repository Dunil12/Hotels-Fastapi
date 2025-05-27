from pydantic import BaseModel


class RoomAddRequest(BaseModel):
    title: str
    price: int
    description:str | None = None
    quantity: int
    facilities_ids_to_add: list[int] | None = [1,2,3]
    facilities_ids_to_remove: list[int] | None = None

class RoomAdd(BaseModel):
    title: str
    price: int
    description:str | None = None
    quantity: int
    hotel_id: int

class Room(RoomAdd):
    id: int
