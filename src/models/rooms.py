from sqlalchemy import String, ForeignKey

from first_project.src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    description: Mapped[str | None]
    quantity: Mapped[int]