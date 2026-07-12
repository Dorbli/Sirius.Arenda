from pydantic import BaseModel
from enum import Enum

class BookingStatus(str, Enum):
    ACTIVE = "активно"
    CANCELLED = "отменено"

class BookingCreate(BaseModel):
    room_id: str
    date_start: str 
    date_end: str 
    status: BookingStatus = BookingStatus.ACTIVE

class Booking(BookingCreate):
    booking_id: str