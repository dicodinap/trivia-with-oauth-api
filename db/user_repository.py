from models.client import db_client
from models.user_scheme import UserInDB
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from models.user_scheme import UserInDB, User
from users.users_services import get_current_user, authenticate_user, create_access_token


db = db_client['local']
collection = db['users']

router = APIRouter()


def get_user(username: str):
    return collection.find_one({'username': username})


def get_password(username: str):
    user = get_user(username)
    return user['hashed_password']


@router.get('/users/me')
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user.dict()


@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
