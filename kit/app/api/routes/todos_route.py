from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.logger import setup_logger
from app.schemas.todo_request import TodoResponse,TodoRequest
from app.helpers.api_response import *
from app.repositories.todo_repository import *

logger = setup_logger('main_logger', 'app/logs/app.log')

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def store(request: TodoRequest, db: Session = Depends(get_db)):
    response = create_todo(request,db)
    if response is not None:
        return send_success_response(response,status=201)
    else:
        return send_error_response("Something went wrong")

@router.get("/{id}")
def show(id:int,db : Session = Depends(get_db)):
    response = single_todo(id,db)
    if response is not None:
        return send_success_response(response)
    else:
        return send_error_response(data={},message="Data not found",status=404)
