from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    name: str
    age: int | None = None
    email: str
    disabled: bool = None


class UserInDB(User):
    hashed_password: str
