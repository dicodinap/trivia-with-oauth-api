from models.user_scheme import User, UserInDB
from db import user_repository


from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated

# Arreglar el authenticate user por el hashed y hacer el login
SECRET_KEY = "iiRavJy8rLmsu5QZ7Sj5SDk4KCJphyep8wi1PvEkzZ8"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schem = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str):
    user = user_repository.get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user_repository.get_password(user)):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    to_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return to_encode


async def get_current_user(token: Annotated[str, Depends(oauth2_schem)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_repository.get_user(username)
    return user


async def get_current_user_active(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_me(current_user: Annotated[User, Depends(get_current_user_active)]):
    return current_user
