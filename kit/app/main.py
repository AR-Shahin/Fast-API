from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import setup_logger
from app.api.routes import users, items, todos
from app.core.database import Base, engine

app = FastAPI(title=settings.PROJECT_NAME)

logger = setup_logger('main_logger', 'app/logs/app.log')

routers: (str, str, str) = [
    (users.router, "/users", "users"),
    (items.router, "/items", "items"),
    (todos.router, "/todos", "todos")
]

for router, prefix, tag in routers:
    app.include_router(router, prefix=prefix, tags=[tag])


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()


@app.get("/")
async def root():
    data = {
        "name": "Shahin",
        "age": 20
    }
    logger.info("Hello shahin")
    return {"message": "Welcome to FastAPI!"}
