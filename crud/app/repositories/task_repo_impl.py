
from .interfaces.task_repository import TaskRepository as Contract
from sqlalchemy.orm import Session
from app.models.Task import Task
from app.schemas.task import TaskSchema

class TaskRepository(Contract):
    
    def __init__(self,db: Session) -> None:
        super().__init__()
        self.db = db
        
    async def create(self, task:TaskSchema) -> Task:
        t = Task()
        t.title = task.title
        t.user_id = 1

        await self.db.add(t)
        self.db.commit()
        
        return t