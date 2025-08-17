from datetime import date
from pydantic import BaseModel


class BookingEmailData(BaseModel):
    user_email: str
    booking_id: int
    room_id: int
    hotel_name: str
    room_name: str
    date_from: date
    date_to: date
    price: int