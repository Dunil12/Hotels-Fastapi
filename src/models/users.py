from sqlalchemy import String

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200), unique=True)
    username: Mapped[str | None] = mapped_column(String(200))
    first_name: Mapped[str | None] = mapped_column(String(200))
    second_name: Mapped[str | None] = mapped_column(String(200))
    phone_number: Mapped[str | None] = mapped_column(String(11))

