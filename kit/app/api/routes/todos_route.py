from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.core.logger import setup_logger
from app.models import Todo
from app.schemas.todo_request import TodoResponse
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
    priority: int = 1
    description: Union[str | None]


@router.post("/", response_model=TodoResponse)
def todos(request: TodoRequest, db: Session = Depends(get_db)):
    db_item = Todo(title=request.title,priority=request.priority)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return 1
