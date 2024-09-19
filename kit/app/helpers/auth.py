from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.helpers.jwt import verify_token
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(data: str = Depends(oauth2_scheme)):
    return verify_token(data)

