# File: app/main.py
from fastapi import FastAPI
from app.api.routes import items, users
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

# File: app/core/config.py


# File: app/core/database.py


# File: app/models/user.py


# File: app/models/todo_repository.py


# File: app/schemas/user.py


# File: app/schemas/todo_repository.py


# File: app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# File: app/crud/todo_repository.py
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# File: app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import User, UserCreate
from app.core.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# File: app/api/routes/items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import item as item_crud
from app.schemas.item import Item, ItemCreate
from app.core.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}/items", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return item_crud.create_user_item(db=db, item=item, user_id=user_id)

@router.get("/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_crud.get_items(db, skip=skip, limit=limit)
    return items

