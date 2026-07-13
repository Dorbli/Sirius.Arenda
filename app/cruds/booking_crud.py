from database.database import get_db
from models.booking_models import BookingStatus
from datetime import datetime as dt
from cruds.rooms_crud import get_room_by_id

def get_all_bookings():
    with get_db() as conn:
        return conn.execute("SELECT * FROM bookings WHERE 1=1").fetchall()

def get_booking_by_id(booking_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM bookings WHERE booking_id = ?",
                           (booking_id,)).fetchone()
        return row

def exist_booking_by_id(booking_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM bookings WHERE booking_id = ?",
                           (booking_id,)).fetchone()
        return dict(row)

def booking_exist(room_id: str, date_start: str, date_end: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM bookings WHERE room_id = ? AND ? < date_end AND ? > date_start AND status = ?",
                           (room_id, date_start, date_end, BookingStatus.ACTIVE)).fetchone()
        if row is not None:
            return '409'
            
def create_booking_in_db(booking_id: str, room_id: str, date_start: str, date_end: str, username: str):
    with get_db() as conn:
        try:
            dt.strptime(date_start, "%Y-%m-%d %H:%M:%S")
            dt.strptime(date_end, "%Y-%m-%d %H:%M:%S")
            
            conn.execute("INSERT INTO bookings (booking_id, room_id, date_start, date_end, username, status) VALUES (?, ?, ?, ?, ?, ?)", 
                        (booking_id, room_id, date_start, date_end, username, BookingStatus.ACTIVE))
            conn.commit()
        except ValueError:
            return '400'
        
def get_bookings_by_date(room_id: str, date: str):
    with get_db() as conn:
        try:
            dt.strptime(date, "%Y-%m-%d")
            rows = conn.execute("SELECT * FROM bookings WHERE room_id = ? AND date(date_start) = ? AND status = ?",
                             (room_id, date, BookingStatus.ACTIVE)).fetchall()
            if rows is None:
                return '404'
            return rows
        except ValueError:
            return '400'

def cancel_booking_in_db(booking_id: str, username: str):
    with get_db() as conn:
        if exist_booking_by_id(booking_id)["username"] == username:
            conn.execute("UPDATE bookings SET status = ? WHERE booking_id = ?",
                        (BookingStatus.CANCELLED, booking_id))
            conn.commit()
        else:
             return '404'
    
def exsist_room_by_id(room_id: str):
    return get_room_by_id(room_id)