from fastapi import APIRouter,Request,Depends
from app.models import TaskModel
from app.config.database import engine
from app.config.Oauth2 import get_current_user
from app.schemas.UserSchema import UserSchema

TaskModel.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404:{"description":"Not found"}}
)

@router.get("/")
def all(get_current_user: UserSchema = Depends(get_current_user)):
    return "All tsk"
