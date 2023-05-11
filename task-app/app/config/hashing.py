from passlib.context import CryptContext
from typing import Union

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    

class Hash:
    
    def bcrypt(password : Union[str,int]):
        return pwd_context.hash(str(password)) 
    
    def verify(plain_password, hashed_password):
        return pwd_context.verify(str(plain_password), hashed_password)