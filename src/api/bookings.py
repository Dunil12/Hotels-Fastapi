from fastapi import Query, APIRouter

from first_project.src.api.dependencies import DBDep, UserIdDep, PaginationDep
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
    price = (await db.rooms.get_one_or_none(id=booking_data.room_id)).price
    _booking_data = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
