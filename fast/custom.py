from fastapi import FastAPI, Depends, HTTPException, status, Header, Request,APIRouter
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone
import random
import string
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

from my_log import logger


bangladesh_timezone = timezone(timedelta(hours=6))

# --- Database Setup ---
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/fastapi"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Security Setup ---

ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 2

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Models (SQLAlchemy) ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    api_token = Column(String(100), unique=True)
    token_timestamp = Column(DateTime)
    refresh_token = Column(String(100), unique=True,nullable=True)
    refresh_token_timestamp = Column(DateTime,nullable=True)

# --- Pydantic Schemas ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# --- Utility Functions ---

def generate_refresh_token(user_id: int, length=32, timestamp: Optional[float] = None) -> str:
    """Generate a random API token with an expiration timestamp."""
    if timestamp is None:

        timestamp = datetime.now(bangladesh_timezone).timestamp()

    expiration_timestamp = timestamp + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    token = f"{timestamp}:{expiration_timestamp}:{random_str}"

    return token

def generate_api_token(user_id: int, length=32, timestamp: Optional[float] = None) -> str:
    """Generate a random API token with an expiration timestamp."""
    if timestamp is None:

        timestamp = datetime.now(bangladesh_timezone).timestamp()

    expiration_timestamp = timestamp + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    token = f"{timestamp}:{expiration_timestamp}:{random_str}"

    return token

def get_current_user(api_token: str, db: Session = Depends(get_db)):
    """Get user based on API token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_timestamp, expiration_timestamp, _ = api_token.split(":")
        token_timestamp = float(token_timestamp)
        expiration_timestamp = float(expiration_timestamp)
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.api_token == api_token).first()
    if user is None:
        raise credentials_exception

    current_timestamp = datetime.now(bangladesh_timezone).timestamp()

    if current_timestamp > expiration_timestamp:
        user_refresh_token = user.refresh_token
        rtoken_timestamp, rexpiration_timestamp, _ = user_refresh_token.split(":")
        rtoken_timestamp = float(rtoken_timestamp)
        rexpiration_timestamp = float(rexpiration_timestamp)
        if current_timestamp > rexpiration_timestamp:
            logger.info("Expired all tokens")
            raise credentials_exception




    return user

# --- FastAPI App ---
app = FastAPI()

# --- Middleware to Check Auth Token ---
@app.middleware("http")
async def check_auth_token(request: Request, call_next):
    exempt_routes = ["/login", "/register","/"]

    if request.url.path in exempt_routes:
        return await call_next(request)

    api_token = request.headers.get("Authorization")
    print("------------------SHAHIN---------------")
    if api_token:
        api_token = api_token.split("Bearer ")[-1]
        try:

            db = SessionLocal()
            user = get_current_user(api_token, db)

            request.state.user = user
            print(f"User authenticated: {user.username}")
        except HTTPException as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid or expired token"}
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "No Authorization token found"}
        )

    # Step 4: Continue processing the request
    response = await call_next(request)
    return response


# --- Create User & Generate Token ---
@app.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = hash_password(user.password)
    api_token = generate_api_token(user_id=0)
    refresh_token = generate_refresh_token(user_id=0)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        api_token=api_token,
        token_timestamp=datetime.now(bangladesh_timezone),
        refresh_token = refresh_token,
        refresh_token_timestamp = datetime.now(bangladesh_timezone)

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User Register -> {new_user.email}")
    return {"access_token": api_token, "refresh_token": refresh_token,"token_type": "bearer"}

# --- Login User & Generate Token ---
@app.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    custom_timestamp = datetime.now(bangladesh_timezone).timestamp()
    api_token = generate_api_token(user_id=db_user.id, timestamp=custom_timestamp)
    refresh_token = generate_refresh_token(user_id=db_user.id, timestamp=custom_timestamp)

    db_user.api_token = api_token
    db_user.refresh_token = refresh_token
    db_user.token_timestamp = datetime.now(bangladesh_timezone)
    db_user.refresh_token_timestamp = datetime.now(bangladesh_timezone)
    db.commit()
    logger.info(f"User Login -> {db_user.email}")
    return {"access_token": api_token,  "refresh_token": refresh_token,"token_type": "bearer"}

# --- Get User Info (Authenticated Route) ---
@app.get("/users/me", response_model=UserResponse)
def get_user_info(api_token: str = Header(...), db: Session = Depends(get_db)):
    current_user = get_current_user(api_token=api_token, db=db)
    return current_user




@app.get("/test")
def test(request: Request):
    current_user = getattr(request.state, "user", None)
    logger.info("current_user")
    if current_user:
        return {"msg": f"Test router {current_user.email}"}
    else:
        return {
            "mgs" : "nai"
        }


@app.get("/")
def test(request: Request):
    logger.info("hello FAST API")
    return {"msg": f"Hello Fast API"}


from fastapi import Form,File,UploadFile
from typing import Annotated


class FormData(BaseModel):
    name: str
    password: str
@app.get("/user")
def user(user:Annotated[FormData , Form()]):
    logger.info("hello FAST API")
    return {"msg": f"Hello Fast API {user}"}


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}



class FormData(BaseModel):
    name: str
    password: str
    email: Optional[str] = None
    age: Optional[int] = None


def create_form_data(
    name: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    age: Optional[int] = Form(None)
) -> FormData:
    return FormData(name=name, password=password, email=email, age=age)


@app.post("/update-data")
async def update_data(
    form_data: FormData = Depends(create_form_data),
    file: UploadFile = File(...)
):

    file_content = await file.read()

    return {
        "data": form_data.dict(),
        "file_size": len(file_content)
    }
