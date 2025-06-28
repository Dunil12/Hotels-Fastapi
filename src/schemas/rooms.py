from pydantic import BaseModel, ConfigDict

from first_project.src.schemas.facility import Facility


class RoomAddRequest(BaseModel):
    title: str
    price: int
    description:str | None = None
    quantity: int
    facilities_ids_to_add: list[int] = []
    facilities_ids_to_remove: list[int] = []

class RoomAdd(BaseModel):
    title: str
    price: int
    description:str | None = None
    quantity: int
    hotel_id: int

class Room(RoomAdd):
    id: int

class RoomWithRels(Room):
    facilities: list[Facility]

    class Config:
        orm_mode = True
