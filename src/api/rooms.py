from fastapi import APIRouter

from first_project.src.api.dependencies import DBDep
from first_project.src.database import async_session_maker
from first_project.src.repositories.rooms import RoomsRepository
from first_project.src.schemas.rooms import Room, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_all_rooms(
        db: DBDep,
        hotel_id: int
) -> list[Room]:
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение отеля по hotel_id, room_id")
async def get_room_by_id(
        db: DBDep,
        hotel_id: int,
        room_id: int,
) -> Room | None:
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Создание записи DB rooms")
async def create_room(
        db: DBDep,
        data: RoomAdd
):
    await db.rooms.add(data)
    await db.commit()

    return {"status" : "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return result


@router.patch("{hotel_id}/rooms/{room_id}")
async def change_room(
        db: DBDep,
        new_room_data: RoomPatch,
        hotel_id: int,
        room_id: int,
):
    changed_room = await db.rooms.change(new_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return changed_room