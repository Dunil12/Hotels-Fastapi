from first_project.src.schemas.hotels import Hotel
from sqlalchemy import select, insert

from first_project.src.models.hotels import HotelsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.hotels import HotelPatch


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
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
