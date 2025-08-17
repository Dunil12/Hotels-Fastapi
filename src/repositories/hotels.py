from datetime import date

from sqlalchemy import select

from src.exceptions import CheckinDateLaterThanCheckoutDateException, ObjectNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel] | None:
        query = select(HotelsOrm)

        if location:
            query = (query
                .filter(HotelsOrm
                .location.contains(location)))
        if title:
            query = (query
                .filter(HotelsOrm
                .title.contains(title)))

        query = (query
                .limit(limit)
                .offset(offset))

        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        hotels = result.scalars().all()

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in hotels]

    async def get_filtered_by_date(
            self,
            title,
            location,
            limit,
            offset,
            date_from: date,
            date_to: date,
    ):
        # перенести валидацию в схему Date_range
        if date_to < date_from:
            raise CheckinDateLaterThanCheckoutDateException

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))

        if title:
            query = (query.filter(HotelsOrm.title.contains(title)))

        if location:
            query = (query.filter(HotelsOrm.location.contains(location)))

        query = (query
                .limit(limit)
                .offset(offset))

        result = await self.session.execute(query)
        hotels = result.scalars().all()
        if not hotels:
            raise ObjectNotFoundException

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in hotels]
