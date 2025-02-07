from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from .config import settings

SECRET_KEY = settings.SECRET_KEY
API_KEY = settings.BACKEND_API_KEY
ALGORITHM = settings.ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login",auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key",auto_error=False)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Admin(BaseModel):
    username: str
    disabled: Optional[bool] = None

ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = pwd_context.hash(settings.ADMIN_PASSWORD)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_admin(username: str):
    if username == ADMIN_USERNAME:
        return Admin(username=username)
    return None

def authenticate_admin(username: str, password: str):
    admin = get_admin(username)
    if not admin:
        return False
    if not verify_password(password, ADMIN_PASSWORD):
        return False
    return admin

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    admin = get_admin(username=token_data.username)
    if admin is None:
        raise credentials_exception
    return admin

async def get_auth(
    jwt_token: Optional[str] = Depends(oauth2_scheme),
    api_key: Optional[str] = Security(api_key_header),
):
    if jwt_token:
        return await get_current_admin(jwt_token)
    elif api_key:
        return await verify_api_key(api_key)
    raise HTTPException(
        status_code=401,
        detail="Either JWT token or API key is required",
        headers={"WWW-Authenticate": "Bearer"},
    )

def add_auth_routes(app: FastAPI):
    @app.post("/login", response_model=Token)
    async def login(form_data: OAuth2PasswordRequestForm = Depends()):
        admin = authenticate_admin(form_data.username, form_data.password)
        if not admin:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": admin.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}