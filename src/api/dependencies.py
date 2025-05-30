
from typing import Annotated
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from first_project.src.database import async_session_maker
from first_project.src.services.auth import AuthService
from first_project.src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)] = 5

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    access_token = request.cookies.get("access_token") or None
    if not access_token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен")
    return access_token

def get_current_user_id(token: str = Depends(get_token)):
    undecoded_token = AuthService().decode_token(token=token)
    return undecoded_token.get("user_id")

UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]