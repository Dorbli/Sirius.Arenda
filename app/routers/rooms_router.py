from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import Optional, List
import uuid
from models.rooms_models import RoomCreate, Room
from cruds.rooms_crud import *
from routers.auth_router import get_user_from_cookie

router = APIRouter(tags=["rooms"])

@router.post("/rooms", response_model=Room, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, curr_user: dict = Depends(get_user_from_cookie)):
    if curr_user["role"] != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Вам не хватает прав")
    
    if room_exists(room.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f'Комната с названием "{room.name}" уже существует'
        )
    
    room_id = str(uuid.uuid4())
    create_room_in_db(room_id, room.name, room.capacity, room.equipment)
    return get_room_by_id(room_id)

@router.get("/rooms", response_model=List[Room])
def get_rooms(min_cap: Optional[int] = Query(None, ge=0),
            max_cap: Optional[int] = Query(None, ge=0),
            equipment: Optional[str] = None):

    if min_cap and max_cap and min_cap > max_cap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Минимальная вместимость не может быть больше максимальной")
    
    rooms = get_all_rooms_with_filters(min_cap, max_cap)

    if equipment:
        rooms = [r for r in rooms if equipment in r["equipment"]]
    
    return rooms

@router.get("/rooms/{room_id}", response_model=Room)
def get_room(room_id: str):
    room = get_room_by_id(room_id)
    if room == '404':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Комната не найдена")
    return room

@router.put("/rooms/{room_id}", response_model=Room)
def update_room(room_id: str, room: RoomCreate, curr_user: dict = Depends(get_user_from_cookie)):
    if curr_user["role"] != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Вам не хватает прав")

    if get_room_by_id(room_id) == '404':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Комната не найдена")
    
    if room_exists(room.name) == '409':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f'Комната с названием "{room.name}" уже существует')
    
    update_room_in_db(room_id, room.name, room.capacity, room.equipment)
    return get_room_by_id(room_id)

@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: str, curr_user: dict = Depends(get_user_from_cookie)):
    if curr_user["role"] != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Вам не хватает прав")
    
    if delete_room_in_db(room_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Комната не найдена")