from sqlalchemy import select, insert
from pydantic import BaseModel, EmailStr

from first_project.src.models.users import UsersOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.users import User, UserWithHashedPassword



class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_or_none(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model:
            return UserWithHashedPassword.model_validate(model, from_attributes=True)
        else:
            return None

