from sqlalchemy import Column, Integer, String, Text,Boolean,ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    priority = Column(Integer, default=0)
    status = Column(Boolean, default=0)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="todos")

