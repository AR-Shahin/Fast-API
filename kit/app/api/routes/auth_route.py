from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import get_user_by_email
from app.helpers.api_response import *
from app.helpers.hashing import *
from app.helpers.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return create_access_token({"sub" : "ars"})
    user = get_user_by_email(db, request.email)

    if user is None:
        return send_success_response(message="User not found!", status=status.HTTP_404_NOT_FOUND)

    if not hash_verify(request.password, user.password):
        return send_error_response({},"Incorrect Password",status.HTTP_204_NO_CONTENT)

    data = {
        "user": user,
        "token": create_access_token(data={"sub": user.email})
    }
    return send_error_response(data, "Authentication successfully!",200)

