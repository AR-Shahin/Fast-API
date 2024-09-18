from sqlalchemy.orm import Session,joinedload
from app.models import Todo
from app.schemas.todo_request import TodoRequest
from app.models.Todo import Todo
from app.core.logger import setup_logger
logger = setup_logger('main_logger', 'app/logs/app.log')

def create_todo(request: TodoRequest, db: Session):
    try:
        db_item = Todo(title=request.title,priority=request.priority,description=request.description,user_id=request.user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        logger.info(e)
        return None


def get_todos(db: Session, skip, limit):
    return db.query(Todo).offset(skip).limit(limit).all()


def single_todo(id: int,db: Session):
    todo = db.query(Todo).options(joinedload(Todo.user)).filter(Todo.id == id).first()

    return todo if todo else None
