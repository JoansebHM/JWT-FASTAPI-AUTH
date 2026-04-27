from datetime import datetime

from fastapi import FastAPI

from app.schemas import UserCreate

app = FastAPI()


@app.get("/")
async def get_data():
    return {"message": "Hello world"}


@app.post("/register")
async def register(user: UserCreate):
    return {
        "message": "User created successfully",
        "email": user.email,
        "created_at": datetime.now(),
    }
