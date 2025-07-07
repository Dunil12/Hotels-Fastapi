from fastapi import HTTPException
from sqlalchemy import select

from first_project.src.exceptions import AllRoomsBookedException
from first_project.src.models.bookings import BookingsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.repositories.utils import rooms_ids_for_booking
from first_project.src.schemas.bookings import Booking, BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_all(
            self,
            limit: int | None = None,
            offset: int | None = None,
            user_id: int | None = None,
    ) -> list[Booking]:
        if user_id:
            query = select(BookingsOrm).filter_by(user_id=user_id)
        else:
            query = select(BookingsOrm)

        query = (query
                 .limit(limit)
                 .offset(offset))

        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        bookings = result.scalars().all()

        return [Booking.model_validate(booking, from_attributes=True) for booking in bookings]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking

        raise AllRoomsBookedException
