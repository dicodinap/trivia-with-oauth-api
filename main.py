<<<<<<< HEAD
from fastapi import FastAPI, Depends, HTTPException, status
from db import user_repository


app = FastAPI()


app.include_router(user_repository.router)
=======
from fastapi import FastAPI, Depends, HTTPException, status
from db.user_repository import user_repository


app = FastAPI()


app.include_router(user_repository.router)
>>>>>>> c7fa32351ddd93ab10857097d2d687b0c7a3d175
