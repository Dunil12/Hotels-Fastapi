from datetime import date

from first_project.src.api.dependencies import UserIdDep
from first_project.src.schemas.bookings import BookingAdd, BookingAddRequest, BookingPatch
from first_project.tests.conftest import db


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(user_id=user_id,
                              price=100,
                              date_from=date(year=2024, month=8, day=2),
                              date_to=date(year=2024, month=8, day=15),
                              room_id=room_id)
    await db.bookings.add(booking_data)

    new_booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert new_booking.price == 100
    assert new_booking.date_from == date(year=2024, month=8, day=2)
    assert new_booking.date_to == date(year=2024, month=8, day=15)


    # update
    new_booking_data = BookingPatch(date_from=date(year=2024, month=8, day=1),
                                    date_to=date(year=2024, month=8, day=16),
                                    price=50)
    new_booking = await db.bookings.change(new_booking_data, user_id=user_id, room_id=room_id)

    print("new_booking = ",new_booking)
    assert new_booking.price == 50
    assert new_booking.date_from == date(year=2024, month=8, day=1)
    assert new_booking.date_to == date(year=2024, month=8, day=16)


    # удалим
    await db.bookings.delete(user_id=user_id, room_id=room_id)
    deleted_booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)

    assert deleted_booking is None


    await db.commit()
