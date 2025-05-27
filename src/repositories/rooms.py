from datetime import date

from first_project.src.models.rooms import RoomsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.rooms import Room
from first_project.src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))


    # async def delete_batch(self, *filter, **filter_by):


