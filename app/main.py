from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import User as UserModel
from app.schemas import User as UserSchema
from app.schemas import UserCreate, UserUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def get_data():
    return {"message": "Hello world"}


@app.get("/users", response_model=List[UserSchema])
async def find_all(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()

    return users


@app.get("/users/{user_id}", response_model=UserSchema)
async def find_one(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return user


@app.patch("/users/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    user = await find_one(user_id, db)

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="This email is already registered")

    new_user = UserModel(
        email=user.email, hashed_password=user.password, full_name=user.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
