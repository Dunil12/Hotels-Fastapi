from datetime import timedelta, datetime, timezone

from jwt import InvalidTokenError
from passlib.context import CryptContext

from first_project.src.config import settings

import jwt
from fastapi import Query, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str):
         try:
             return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
         except jwt.exceptions.DecodeError:
             raise HTTPException(status_code=401, detail="неверный токен")