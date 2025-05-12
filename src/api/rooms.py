from fastapi import APIRouter

from first_project.src.database import async_session_maker
from first_project.src.repositories.rooms import RoomsRepository
from first_project.src.schemas.rooms import Room, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_all_rooms(hotel_id: int) -> list[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение отеля по hotel_id, room_id")
async def get_room_by_id(
        hotel_id: int,
        room_id: int,
) -> Room | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Создание записи DB rooms")
async def create_room(
        data: RoomAdd
):
    async with async_session_maker() as session:
        await RoomsRepository(session).add(data)
        await session.commit()

    return {"status" : "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with (async_session_maker() as session):
        result = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return result


@router.patch("{hotel_id}/rooms/{room_id}")
async def change_room(
        new_room_data: RoomPatch,
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        changed_room = await RoomsRepository(session).change(new_room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
        return changed_room