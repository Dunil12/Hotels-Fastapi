import typing
from datetime import date
from pydantic import BaseModel, field_validator

from src.exceptions import CheckinDateLaterThanCheckoutDateHTTPException

if typing.TYPE_CHECKING:
    from pydantic_core.core_schema import ValidationInfo


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int

    @field_validator("date_to")
    @classmethod
    def validate_dates(cls, date_to: date, info: "ValidationInfo") -> date:
        """
        Проверяет, что date_to не раньше date_from.
        """
        date_from = info.data.get("date_from")
        if date_from and date_to < date_from:
            raise CheckinDateLaterThanCheckoutDateHTTPException
        return date_to

class BookingAdd(BookingAddRequest):
    user_id: int
    price: int

class BookingPatch(BaseModel):
    date_from: date | None
    date_to: date | None
    price: int | None

class Booking(BookingAdd):
    id: int

