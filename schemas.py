from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    date: datetime
    


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class config:
        orm_mode = True
