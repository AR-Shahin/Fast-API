from app.config.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,unique=True, primary_key=True,index=True)
    name = Column(String(length=100),default="Default Name")
    email = Column(String(length=100),unique=True)
    password = Column(String(length=255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime,default=datetime.datetime.now())
    
    tasks = relationship("Task",back_populates="user")
    
    
    