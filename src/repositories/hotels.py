from first_project.src.schemas.hotels import Hotel
from sqlalchemy import select, insert

from first_project.src.models.hotels import HotelsOrm
from first_project.src.repositories.base import BaseRepository



class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
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
    
        return hotels

    # async def add(
    #         self,
    #         hotel_data,
    # ):
    #     add_hotel_stmt = insert(table=self.model).values(**hotel_data.model_dump())
    #     print(hotel_data)
    #     print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
    #
    #     await self.session.execute(add_hotel_stmt)