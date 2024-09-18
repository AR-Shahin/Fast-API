from typing import *

from pydantic import BaseModel


class TodoRequest(BaseModel):
    title: str = "This is a demo todo."
    priority: int = 0
    description: Optional[str | None] = None
    user_id:  str | int = 1


class TodoResponse(TodoRequest):
    id: int
    status: bool

    class Config:
        from_attributes = True
