from sqlalchemy import select

from first_project.src.models.rooms import RoomsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_all(
            self,
            hotel_id: int,
    ) -> list[Room]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        rooms = result.scalars().all()

        return [self.schema.model_validate(room, from_attributes=True) for room in rooms]