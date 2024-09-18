from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.core.logger import setup_logger
from app.models.Todo import Todo
from app.schemas.todo_request import TodoResponse,TodoRequest
from app.helpers.api_response import *
logger = setup_logger('main_logger', 'app/logs/app.log')

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/",response_model= TodoResponse)
def todos(request: TodoRequest, db: Session = Depends(get_db)):
    try:
        db_item = Todo(title=request.title,priority=request.priority,description=request.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        logger.info(e)
        return e
