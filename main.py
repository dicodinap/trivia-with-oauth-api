from fastapi import FastAPI, Depends, HTTPException, status
from db import user_repository


app = FastAPI()


app.include_router(user_repository.router)
