from app.config.database import Base
from sqlalchemy import Column,Integer,String,Float,Boolean,Text,ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key = True, index=True) 
    title = Column(String(length=100))
    duration = Column(Float,default=1.9)
    status = Column(Boolean,default=True)
    description = Column(Text,default="Description")
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User",back_populates="tasks")
