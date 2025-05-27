from sqlalchemy import select, insert, update, delete

from pydantic import BaseModel

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(model, from_attributes=True) if model is not None else None


    async def change(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        change_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(change_stmt)


    async def delete(self, **filter_by):
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        data_db = await self.get_one_or_none(**filter_by)

        if data_db:
            delete_data_stmt = delete(table=self.model).filter_by(**filter_by)
            print(delete_data_stmt.compile(compile_kwargs={"literal_binds": True}))
            await self.session.execute(delete_data_stmt)
            return {"status": "200"}
        else:
            print("запись по входящим параметрам не найдена")
            return {"status" : "404"}


    async def add(self, data: BaseModel):
        print(data)
        add_data_stmt = insert(table=self.model).values(**data.model_dump()).returning(self.model)
        print(add_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)


    async def add_batch(self, data: list[BaseModel]):
        add_data_stmt = insert(table=self.model).values([item.model_dump() for item in data])
        print(add_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_data_stmt)