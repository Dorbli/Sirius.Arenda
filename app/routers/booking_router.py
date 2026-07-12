from fastapi import APIRouter, HTTPException, status, Depends
import uuid
from models.booking_models import BookingCreate
from cruds.booking_crud import *
from routers.auth_router import get_user_from_cookie

router = APIRouter(tags=['bookings'])

@router.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, curr_user: dict = Depends(get_user_from_cookie)):
    if booking_exist(booking.room_id, booking.date_start, booking.date_end) == '409':
        raise HTTPException(status.HTTP_409_CONFLICT,
                             f"Пространство {booking.room_id} на это время занято.")
    if exsist_room_by_id(booking.room_id) == '404':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Комната не найдена")
    
    booking_id = str(uuid.uuid4())
    stat = create_booking_in_db(booking_id, booking.room_id,
                          booking.date_start, booking.date_end, curr_user["username"])
    
    if stat == '400':
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                             "Неверный формат даты. Верный формат: YYYY-MM-DD hh:mm:ss.")
    
    return get_booking_by_id(booking_id=booking_id)

@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booking_id: str, curr_user: dict = Depends(get_user_from_cookie)):
    if cancel_booking_in_db(booking_id, curr_user["username"]) == '404':
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                             f'Бронь под номером {booking_id} не найдена, либо не вы её бронировали.')
    
@router.get("/rooms/{room_id}/bookings")
def get_booking(room_id: str, date: str):
    bookings = get_bookings_by_date(room_id, date)
    if bookings == '404':
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                             f"Броней в комнате с id:{room_id} в {date} нет.")
    if bookings == '400':
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                             "Неверный формат даты. Верный формат: YYYY-MM-DD.")
    return bookings

@router.get("/bookings")
def get_all_books():
    return get_all_bookings()