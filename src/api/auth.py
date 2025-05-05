from fastapi import Query, APIRouter
from passlib.context import CryptContext

from first_project.src.database import async_session_maker
from first_project.src.repositories.users import UsersRepository
from first_project.src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация клиента")
async def register_user(
    user_data: UserRequestAdd
):
    hashed_password = pwd_context.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with (async_session_maker() as session):
        user = await UsersRepository(session).add(new_user_data)
        if user:
            print(user)
            await session.commit()
            return {"status": "OK"}
        else:
            return {"status" : "User already exist"}
