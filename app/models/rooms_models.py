from pydantic import BaseModel, field_validator
from typing import List

class RoomCreate(BaseModel):
    name: str
    capacity: int
    equipment: List[str]
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Название не может быть пустым")
        return value.strip()
    
    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Вместимость должна быть больше нуля")
        return value

class Room(RoomCreate):
    id: str