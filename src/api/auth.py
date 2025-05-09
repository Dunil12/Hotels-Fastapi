from typing import Annotated

import jwt
from fastapi import Query, APIRouter, HTTPException, Response, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer

from first_project.src.api.dependencies import UserIdDep, get_token
from first_project.src.database import async_session_maker
from first_project.src.repositories.users import UsersRepository
from first_project.src.schemas.users import UserRequestAdd, UserAdd
from first_project.src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.get("/test_user_jwt", summary="тест получения пользовтеля из JWT токена")
async def get_current_user(
        user_id: UserIdDep
):
    async with (async_session_maker() as session):
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/register", summary="Регистрация клиента")
async def register_user(
    user_data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with (async_session_maker() as session):
        user = await UsersRepository(session).add(new_user_data)
        if user:
            await session.commit()
            print(user)
            return {"status": "OK"}
        else:
            return {"status" : "Клиент уже существует"}


@router.post("/login", summary="Аутентификация клиента")
async def login_user(
    user_data: UserRequestAdd,
    response: Response,
):

    async with (async_session_maker() as session):
        user = await UsersRepository(session).get_user_or_none(email=user_data.email)
        print("USER = ", user)
        if not user:
            raise HTTPException(status_code=401, detail="Клиент с таким email не зарегестрирован")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Email или пароль неверный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        await session.commit()
        return {"access_token": access_token}


@router.post("/logout")
async def logout(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
