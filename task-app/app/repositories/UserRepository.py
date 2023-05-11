from sqlalchemy.orm import Session
from app.schemas.UserSchema import UserSchema
from app.models.UserModel import User
from app.config.hashing import Hash


class UserRepository():
    
    def __init__(self,db: Session):
        self.db = db
        
    def all(self):
        users = self.db.query(User).all()
        return users
    
    def create(self, request: UserSchema):
        user = User()
        user.name = request.name
        user.email = request.email
        user.password = Hash.bcrypt(request.password)
        
        self.db.add(user)
        self.db.commit()
        
        return user
    

        