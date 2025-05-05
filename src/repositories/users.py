from sqlalchemy import select, insert
from pydantic import BaseModel

from first_project.src.models.users import UsersOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.users import User



class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    # под вопросом BaseModel, возможно стоит -> UserRegister
    async def add1(self, user_data: BaseModel):
        # реализация логики проверки пользователя (вызов метода?)
        # шифрование пароля
        # добавление в бд
        return {"status": "OK"}
