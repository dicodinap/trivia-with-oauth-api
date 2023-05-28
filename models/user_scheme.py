from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    full_name: str
    age: int | None = None
    email: str
    disabled: bool


class UserInDB(User):
    hashed_password: str
