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

# class UserPatch(BaseModel):
#     email: EmailStr | None = Field(None)
#     password: str | None = Field(None)
#     username: str | None = Field(None)
#     first_name: str | None = Field(None)
#     second_name: str | None = Field(None)
#     phone_number: str | None = Field(None)

