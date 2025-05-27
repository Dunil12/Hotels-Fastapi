from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    title: str

# class RoomPatch(BaseModel):
#     title: str
#     price: int
#     description: str | None = Field(None)
#     quantity: int

class Facility(FacilityAdd):
    id: int




class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacility(RoomFacilityAdd):
    id: int