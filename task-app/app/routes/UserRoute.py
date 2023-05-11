from fastapi import APIRouter,Request,Depends
from app.models import UserModel
from app.config.database import engine
from app.repositories.UserRepository import UserRepository
from app.config.database import SessionLocal
from sqlalchemy.orm import session
from app.schemas.UserSchema import UserSchema,UserSchemaOut
from typing import List


UserModel.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404:{"description":"Not found"}}
)

@router.get("/",response_model=List[UserSchemaOut])
def all(db: session = Depends(get_db)):
    return UserRepository(db).all()

@router.post("/")
async def create(user: UserSchema, db: session = Depends(get_db)):
    
    u = UserRepository(db)
    return u.create(user)
