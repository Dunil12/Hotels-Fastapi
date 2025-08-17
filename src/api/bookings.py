from fastapi import APIRouter
from sqlalchemy.exc import NoResultFound

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import ObjectNotFoundException, AllRoomsBookedException, RoomNotFoundHTTPException, \
    UserNotFoundHTTPException, HotelNotFoundHTTPException, AllRoomsBookedHTTPException
from src.repositories.utils import today_users
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.emails import BookingEmailData
from src.services.reports import AdminReportsService
from src.tasks.emails.emails import send_booking_confirmation_email

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
        raise RoomNotFoundHTTPException

    try:
        hotel = await db.hotels.get_one(id=room.hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    room_price: int = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsBookedException:
        raise AllRoomsBookedHTTPException

    await db.commit()

    try:
        user = await db.users.get_one(id=user_id)
    except NoResultFound:
        raise UserNotFoundHTTPException

    print("booking =", booking.model_dump())
    # Формируем данные для письма
    email_data = BookingEmailData(
        user_email=user.email,
        booking_id=booking.id,
        room_id=room.id,
        hotel_name=hotel.title,
        room_name=room.title,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room_price
    )
    print("email_data =", email_data)

    # Запускаем задачу отправки письма
    send_booking_confirmation_email.delay(email_data=email_data.model_dump())

    return {"status": "OK", "data": booking}


# @router.get("", summary="Получение таблицы excel о сегодняшних клиентах")
# async def get_today_users(
#         db: DBDep,
#         hotel_id: int,
# ):
#     # вывести информацию о пользователях, находящихся в отеле сегодня (или заселяющихся)
#     res = AdminReportsService(db).get_today_users()
#
#     # логика обработки в excel
#     # res = today_users()