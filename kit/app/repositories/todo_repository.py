from sqlalchemy.orm import Session
from app.models import Todo
from app.schemas.todo_request import TodoRequest


def create_todo(todo: TodoRequest, db: Session):
    db_item = Todo(**todo.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_todos(db: Session, skip, limit):
    return db.query(Todo).offset(skip).limit(limit).all()


def single_todo(db: Session, id: int):
    todo = db.query(Todo).filter(id=id).first()

    return todo if todo else None
