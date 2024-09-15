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
