from fastapi import APIRouter, HTTPException

from first_project.src.api.dependencies import DBDep, UserIdDep, PaginationDep
from first_project.src.exceptions import ObjectNotFoundException, AllRoomsBookedException
from first_project.src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("", summary="Получение всех записей бронирования",)
async def get_all_bookings(
    pagination: PaginationDep,
    db: DBDep,
):
    print("pagination.per_page)=", pagination.per_page)
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)
    return await db.bookings.get_all(limit=limit, offset=offset)


@router.get("/me", summary="Получение своих записей бронирования",)
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_all(user_id=user_id)


@router.post("")
async def create_booking(
    db: DBDep,
    booking_data: BookingAddRequest,
    user_id: UserIdDep,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")

    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()

    return {"status": "OK", "data": booking}
