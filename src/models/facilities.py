import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from first_project.src.database import Base
if typing.TYPE_CHECKING:
    from first_project.src.models import RoomsOrm


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(back_populates="facilities", secondary="rooms_facilities", )