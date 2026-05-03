from typing import Annotated, List

from fastapi import Depends, FastAPI

from app.core.handlers import add_exception_handlers
from app.core.messages import AuthMessages
from app.crud import UserCRUD
from app.database import Base, engine, DbDep
from app.schemas import LoginSchema
from app.schemas import User as UserSchema
from app.schemas import UserCreate, UserUpdate
from app.models import User as UserModel
from app.core.security import create_access_token, get_current_user, list_users


app = FastAPI()

Base.metadata.create_all(bind=engine)


add_exception_handlers(app)


@app.get("/users", response_model=List[UserSchema])
async def find_all(users: Annotated[List[UserModel], Depends(list_users)]):
    return users


@app.get("/users/me", response_model=UserSchema)
async def find_me(user: Annotated[UserModel, Depends(get_current_user)]):
    return user


@app.get("/users/{user_id}", response_model=UserSchema)
async def find_one(user_id: int, db: DbDep):
    return UserCRUD.get_user_by_id(db=db, user_id=user_id)


@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: DbDep):
    return UserCRUD.update_user(db=db, user_id=user_id, user_update=user_update)


@app.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: DbDep):
    return UserCRUD.delete_user(db=db, user_id=user_id)


@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: DbDep):
    return UserCRUD.create_user(
        db=db, email=user.email, password=user.password, full_name=user.full_name
    )


@app.post("/login")
async def login(data: LoginSchema, db: DbDep):
    user = UserCRUD.is_user_authenticated(db=db, data=data)

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "type": "bearer",
        "message": AuthMessages.LOGIN_SUCCESS,
        "user": {"email": user.email, "full_name": user.full_name},
    }
