from datetime import date
from fastapi import APIRouter, Query

from src.api.dependencies import DBDep
from src.exceptions import CheckinDateLaterThanCheckoutDateException, ObjectNotFoundException, \
    RoomNotFoundHTTPException, HotelNotFoundHTTPException, \
    HotelNotFoundException, RoomNotFoundException, CheckinDateLaterThanCheckoutDateHTTPException
from src.schemas.rooms import RoomAddRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение номеров отеля отфильтрованных по дате")
async def get_rooms_by_date(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-05-10"),
        date_to: date = Query(example="2025-05-11"),
):
    try:
        return await RoomService(db).get_rooms_by_date(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
    except CheckinDateLaterThanCheckoutDateException:
        raise CheckinDateLaterThanCheckoutDateHTTPException
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение отеля по hotel_id, room_id")
async def get_room_by_id(
        db: DBDep,
        room_id: int,
):
    try:
        return await RoomService(db).get_room_by_id(room_id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создание записи DB rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest,
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "Ok", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    try:
        result = await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data_was_deleted": result}


@router.patch("{hotel_id}/rooms/{room_id}")
async def change_room(
        db: DBDep,
        new_room_data: RoomAddRequest,
        hotel_id: int,
        room_id: int,
):
    try:
        await RoomService(db).change_room(
            new_room_data=new_room_data,
            hotel_id=hotel_id,
            room_id=room_id,
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException