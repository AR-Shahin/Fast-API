from fastapi import FastAPI
from app.routes import TaskRoute,UserRoute,AuthRoute
from app.config.hashing import Hash




app = FastAPI(
    debug=True,
    title="Task API",
    version=1.0
)

app.include_router(AuthRoute.router)
app.include_router(UserRoute.router)
app.include_router(TaskRoute.router)


@app.get("/",summary="Application Root URL")
def index():
    a=  Hash.bcrypt("123");
    
    return Hash.verify(1237,a)