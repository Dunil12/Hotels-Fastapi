from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from first_project.src.models.rooms import RoomsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.rooms import Room, RoomWithRels
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

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        res = [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

        print(res)
        return res
        # return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return RoomWithRels.model_validate(model, from_attributes=True) if model is not None else None