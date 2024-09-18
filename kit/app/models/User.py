from sqlalchemy import *
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True,)
    password = Column(String(255))
    status = Column(Boolean, default=True)


    todos = relationship('Todo', back_populates="user")

