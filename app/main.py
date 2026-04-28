from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import UserNotFoundError
from app.core.handlers import add_exception_handlers
from app.core.security import get_password_hash, verify_password
from app.database import Base, engine, get_db
from app.models import User as UserModel
from app.schemas import LoginSchema
from app.schemas import User as UserSchema
from app.schemas import UserCreate, UserUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)

DbDep = Annotated[Session, Depends(get_db)]

add_exception_handlers(app)


@app.get("/")
async def get_data():
    return {"message": "Hello world"}


@app.get("/users", response_model=List[UserSchema])
async def find_all(db: DbDep):
    users = db.query(UserModel).filter(UserModel.is_active).all()

    return users


@app.get("/users/{user_id}", response_model=UserSchema)
async def find_one(user_id: int, db: DbDep):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise UserNotFoundError(user_id=user_id)

    return user


@app.patch("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_update: UserUpdate, db: DbDep):
    user = await find_one(user_id=user_id, db=db)

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            setattr(user, "hashed_password", value)
        else:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: DbDep):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    setattr(user, "is_active", False)
    db.commit()
    db.refresh(user)

    return user


@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: DbDep):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="This email is already registered")

    new_user = UserModel(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
async def login(data: LoginSchema, db: DbDep):
    user = (
        db.query(UserModel)
        .filter(UserModel.email == data.email, UserModel.is_active)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if verify_password(
        plain_password=data.password, hashed_password=user.hashed_password
    ):
        return {"message": "Welcome again!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
