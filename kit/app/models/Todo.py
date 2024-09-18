from sqlalchemy import Column, Integer, String, Text,Boolean
from app.core.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(Integer, default=0)
    status = Column(Boolean, default=0)
    description = Column(Text, nullable=True)