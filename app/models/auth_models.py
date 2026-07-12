from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class User_in_db(User):
    hashed_password: str
    user_id: str

class User_url(BaseModel):
    username: str
    password: str
    role: str = 'base'