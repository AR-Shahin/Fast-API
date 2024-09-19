from pydantic import BaseModel
from typing import List, Union
from app.schemas.todo_request import TodoResponse


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    status: bool

    todos: List[TodoResponse] = []

    class Config:
        from_attributes = True
