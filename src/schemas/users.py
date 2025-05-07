from pydantic import BaseModel, EmailStr

class UserRequestAdd(BaseModel):
    email: EmailStr | None
    password: str | None

class User(BaseModel):
    id: int | None
    email: EmailStr | None
    username: str | None
    first_name: str | None
    second_name: str | None
    phone_number: str | None

class UserAdd(BaseModel):
    email: EmailStr | None
    hashed_password: str | None

class UserWithHashedPassword(BaseModel):
    id: int | None
    email: EmailStr | None
    hashed_password: str | None
