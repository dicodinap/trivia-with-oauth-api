from models.client import db_client
from models.user_scheme import UserInDB
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from models.user_scheme import UserInDB, User
from users.users_services import get_current_user, authenticate_user, create_access_token


db = db_client['local']
collection = db['users']

router = APIRouter()


def get_user(username: str):
    user = collection.find_one({'username': username})
    return user


def get_user_db(username: str):
    user = collection.find_one({'username': username})
    return UserInDB(**user)


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


@router.post('/create', response_model=UserInDB)
async def create_user(user: UserInDB):
    user_dict = dict(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Credential not allowed")
    id = collection.insert_one(user_dict).inserted_id

    return {"message": "Your account has been created", "id": str(id), "user": user_dict}
