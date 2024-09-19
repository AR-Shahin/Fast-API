from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import setup_logger
from app.api.routes import users_route, todos_route,auth_route
from app.core.database import Base, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.seeders.user_seeder import create

app = FastAPI(title=settings.PROJECT_NAME)

logger = setup_logger('main_logger', 'app/logs/app.log')

routers: (str, str, str) = [
    (auth_route.router, "/auth", "Authentication"),
    (users_route.router, "/users", "User"),
    (todos_route.router, "/todos", "Todo")
]

for router, prefix, tag in routers:
    app.include_router(router, prefix=prefix, tags=[tag])


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()


@app.get("/")
async def root():
    # init_db()
   #  create()
    data = {
        "name": "Shahin",
        "age": 20
    }

    return {"message": "Welcome to FastAPI!"}
