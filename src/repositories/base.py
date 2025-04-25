from sqlalchemy import select, insert
from first_project.src.schemas.hotels import Hotel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, *args, **kwargs): # добавить вместо hotel_data -> BaseModel sqlAlchemy (схема)
        # add_hotel_stmt = insert(table=self.model).values(hotel_data.model_dump())
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        # await self.session.execute(add_hotel_stmt)
        # await self.session.commit()
        return {"status": "OK"}
