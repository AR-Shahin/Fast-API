from pydantic import BaseModel
from typing import List
from app.schemas.item import Item

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attributes = True