from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user_request import UserCreate
from app.helpers.hashing import *
from sqlalchemy import desc


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).order_by(desc(User.id)).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, password=bcrypt(user.password), status=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return None
