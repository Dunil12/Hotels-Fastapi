from datetime import date
from urllib.parse import uses_query

from pydantic import BaseModel
from sqlalchemy import insert, select

from first_project.src.models.bookings import BookingsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.bookings import Booking


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

