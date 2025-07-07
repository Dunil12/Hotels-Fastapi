from datetime import date
from fastapi import APIRouter, Query, HTTPException

from first_project.src.api.dependencies import DBDep
from first_project.src.exceptions import CheckinDateLaterThanCheckoutDateException, ObjectNotFoundException
from first_project.src.schemas.facility import RoomFacilityAdd
from first_project.src.schemas.rooms import RoomAddRequest, RoomAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение номеров отеля отфильтрованных по дате")
async def get_rooms_by_date(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-05-10"),
        date_to: date = Query(example="2025-05-11"),
):
    try:
        return await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    except CheckinDateLaterThanCheckoutDateException:
        raise HTTPException(status_code=400, detail="Дата заезда позже даты выезда")
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение отеля по hotel_id, room_id")
async def get_room_by_id(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    try:
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")


@router.post("/{hotel_id}/rooms", summary="Создание записи DB rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest,
):
    try:
        await db.hotels.get_one(**{"id": hotel_id})
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(facility_id=facility_id, room_id=room.id)
                             for facility_id in room_data.facilities_ids_to_add]
    await db.rooms_facilities.add_batch(rooms_facilities_data)
    await db.commit()

    return {"status": "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    try:
        result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    # добавить логику удаления из roomsTOfacilities записей
    await db.commit()
    return result


@router.patch("{hotel_id}/rooms/{room_id}")
async def change_room(
        db: DBDep,
        new_room_data: RoomAddRequest,
        hotel_id: int,
        room_id: int,
):
    _new_room_data = RoomAdd(hotel_id=hotel_id, **new_room_data.model_dump())
    try:
        await db.rooms.change(_new_room_data, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")

    if new_room_data.facilities_ids_to_remove:
        await db.rooms_facilities.delete_batch(room_id=room_id, facilities_ids = new_room_data.facilities_ids_to_remove)
    if new_room_data.facilities_ids_to_add:
        rooms_facilities_data_to_add = [RoomFacilityAdd(facility_id=facility_id, room_id=room_id)
                                        for facility_id in new_room_data.facilities_ids_to_add]
        await db.rooms_facilities.add_batch(rooms_facilities_data_to_add)

    await db.commit()