from fastapi import FastAPI, Query,Form
from typing import Union,List
from pydantic import BaseModel
from typing_extensions import Annotated
from datetime import datetime, time, timedelta

from app.routers import tasks
from app.models import Task,User
from app.config.database import engine
app = FastAPI(debug=True)

Task.Base.metadata.create_all(bind=engine)
User.Base.metadata.create_all(bind=engine)
app.include_router(tasks.router)

@app.get("/")
def index() :
    return "Hello Shahin!"










# class Item(BaseModel):
#     name : str
#     email : str
#     age : int
#     bio : Union[str, None] = None

# class User(BaseModel):
#     name : Annotated[str,int]
#     email : Annotated[str,int]
#     password : Annotated[str,int]
    
    






# @app.post("/login/")
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#     return {"username": username}

# users = [
#     {
#         "name" : "Shahin",
#         "id" : 1
#     },
#     {
#         "name" : "Omi",
#         "id" : 2
#     },
#     {
#         "name" : "Rasel",
#         "id" : 3
#     },
# ]



# @app.get("/")
# async def index():
#     return "Hello World!"

# @app.get("/users")
# async def all_users():
#     return users

# @app.get("/users/{id}")
# async def single_user(id:int):
#     for user in users:
#         if user["id"] == id:
#             return user
#     return "Not Found!"



# @app.get("/items")
# async def read_item(
#     q : Annotated[Union[str,int,None] , Query(max_length=2)] = None ,
#     p : Union[str, None] = Query(default=None, max_length=50,),
#     r: Annotated[Union[List[str], None], Query()] = None
# ):
#     return {
#         "r" : r
#         };

# async def read_items(
#     q: Annotated[Union[str, None], Query(max_length=50)] = None
#     ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/search/{id}")
# async def search(
#     id :int ,age:int,sort: Union[int,None,str] = None
#     ):
#     return  {age,sort,id}

# @app.post("/items")
# def store(item : Item):
#     return item

# @app.get("/test")
# def test():
#     return {
#             "date" : datetime.now(),
#             "time" : time(),
#         }
    