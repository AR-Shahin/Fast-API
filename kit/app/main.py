from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import setup_logger
from app.api.routes import users,items


app = FastAPI(title=settings.PROJECT_NAME)
logger = setup_logger('main_logger', 'app/logs/app.log')

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    data = {
        "name" : "Shahin",
        "age" : 20
    }
    logger.info("Hello shahin")
    return {"message": "Welcome to FastAPI!"}


