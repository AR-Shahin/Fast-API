from fastapi import APIRouter,Request,Depends,status,HTTPException
from app.models.UserModel import User
from app.config.database import engine
from app.schemas.AuthSchema import LoginSchema
from app.config.database import SessionLocal
from sqlalchemy.orm import session
from app.config.hashing import Hash
from app.config.JWT import JWT
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404:{"description":"Not found"}}
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db:session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        return {
            "status" : status.HTTP_404_NOT_FOUND,
            "mgs" : "User not found!"
        }
    if not Hash.verify(request.password, user.password):
        return {
            "status" : status.HTTP_422_UNPROCESSABLE_ENTITY,
            "mgs" : "Incorrect Password"
        }
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token = JWT.create_access_token({
        "sub" : user.email,
        "expires_delta" : access_token_expires
    })
    return {
            "token" : token,
            "token_type": "bearer"
        }

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),
                                 db: session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    expires_delta = timedelta(minutes=20)
    token  = creat_access_token(user.username, user.id, expires_delta)
    return {"token":token}