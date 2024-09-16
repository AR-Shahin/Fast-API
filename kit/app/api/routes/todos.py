from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import todo as todo_crud
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.core.logger import setup_logger
from app.models import Todo

from app.helpers.api_response import *
logger = setup_logger('main_logger', 'app/logs/app.log')

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = "This is a demo todo."
    priority: int
    description: Union[str | None]


@router.post("/")
def todos(request: TodoRequest):
    todo = Todo()
    todo.title = "hi"
    return todo.title
