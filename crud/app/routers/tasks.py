from fastapi import APIRouter,Depends
from app.config.database import engine,Sessionlocal
from app.schemas import task
# from app.models.Task import Task
from sqlalchemy.orm import Session
from app.repositories.task_repo_impl import TaskRepository
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404:{"description":"Not found"}}
)

# Task.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/",status_code=200)
def all():
    return "all tasks!"

@router.post("/")
def store(task: task.TaskSchema,db:Session = Depends(get_db)):
    t = TaskRepository(db)
    return t.create(task)