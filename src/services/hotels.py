from datetime import date

from sqlalchemy.exc import NoResultFound

from src.api.dependencies import PaginationDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_hotels(
            self,
            pagination: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ):

        limit = pagination.per_page or 5
        offset = limit * (pagination.page - 1)

        return await self.db.hotels.get_filtered_by_date(
            title=title,
            location=location,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to,
        )


    async def get_hotel_by_id(self, hotel_id: int):
        try:
            return await self.db.hotels.get_one(**{"id": hotel_id})
        except ObjectNotFoundException as e:
            raise HotelNotFoundException from e


    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel


    async def delete_hotel(
            self,
            hotel_id: int,
            title: str | None,
            location: str | None
    ):
        hotel = await HotelService(self.db).get_hotel_by_id(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id, title=title, location=location)
        await self.db.commit()
        return hotel

    async def change_hotel(
            self,
            new_hotel_data: HotelPatch,
            hotel_id: int,
            title: str | None,
            location: str | None,
    ):
        try:
            hotel = await self.db.hotels.change(new_hotel_data, id=hotel_id, title=title, location=location)
        except NoResultFound:
            raise HotelNotFoundException
        await self.db.commit()
        return hotel

    # async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
    #     try:
    #         return await self.get_hotel_by_id(hotel_id)
    #     except ObjectNotFoundException:
    #         raise HotelNotFoundException