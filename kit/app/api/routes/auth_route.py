from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import get_user_by_email
from app.helpers.api_response import *
from app.helpers.hashing import *
from app.core.jwt import create_access_token,create_token_pair
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: AuthRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)

    if user is None:
        return send_success_response(message="User not found!", status=status.HTTP_404_NOT_FOUND)

    if not hash_verify(request.password, user.password):
        return send_error_response({},"Incorrect Password",status.HTTP_204_NO_CONTENT)

    data = {
        "user": user,
        "token": create_token_pair(user.email)

    }
    return send_success_response(data, "Authentication successful!",200)


@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    email = payload.get("sub")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    new_access_token = create_access_token({"sub": email})

    return {"access_token": new_access_token}

@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
