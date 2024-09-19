from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import *
from app.schemas.user_request import UserResponse, UserCreate
from app.core.database import SessionLocal
from app.core.logger import setup_logger
from app.helpers.api_response import *
from typing import List
from app.helpers.auth import get_current_user

logger = setup_logger('main_logger', 'app/logs/app.log')

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return send_error_response({}, "User Already exists!", 422)
    return send_success_response(create_user(db=db, user=user), "User Created Successfully", 201)


@router.get("/")
def index(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: UserCreate = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    users = [UserResponse.from_orm(user) for user in users]
    return send_success_response(users, status=200)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return send_success_response({}, "User Deleted", status.HTTP_204_NO_CONTENT)
