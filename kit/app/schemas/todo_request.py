from typing import *

from pydantic import BaseModel


class TodoRequest(BaseModel):
    title: str = "This is a demo todo."
    priority: int
    description: Union[str | None]


class TodoResponse(TodoRequest):
    id: int
    status: bool

    class Config:
        from_attributes = True
