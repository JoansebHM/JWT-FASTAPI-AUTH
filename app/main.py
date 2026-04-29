from typing import Annotated, List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError, UserNotFoundError
from app.core.handlers import add_exception_handlers
from app.core.messages import AuthMessages, UserMessages
from app.core.security import get_password_hash, verify_password
from app.crud import UserCRUD
from app.database import Base, engine, get_db
from app.models import User as UserModel
from app.schemas import LoginSchema
from app.schemas import User as UserSchema
from app.schemas import UserCreate, UserUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)

DbDep = Annotated[Session, Depends(get_db)]

add_exception_handlers(app)


@app.get("/users", response_model=List[UserSchema])
async def find_all(db: DbDep):
    return UserCRUD.get_all_users(db=db)


@app.get("/users/{user_id}", response_model=UserSchema)
async def find_one(user_id: int, db: DbDep):
    return UserCRUD.get_user_by_id(db=db, user_id=user_id)


@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: DbDep):
    user = await find_one(user_id=user_id, db=db)

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return UserMessages.UPDATED


@app.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: DbDep):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise UserNotFoundError()

    setattr(user, "is_active", False)
    db.commit()
    db.refresh(user)

    return UserMessages.DELETED


@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: DbDep):
    return UserCRUD.create_user(
        db=db, email=user.email, password=user.password, full_name=user.full_name
    )


@app.post("/login")
async def login(data: LoginSchema, db: DbDep):
    user = (
        db.query(UserModel)
        .filter(UserModel.email == data.email, UserModel.is_active)
        .first()
    )

    if not user:
        raise InvalidCredentialsError()
    if not verify_password(
        plain_password=data.password, hashed_password=user.hashed_password
    ):
        raise InvalidCredentialsError()

    return {"message": AuthMessages.LOGIN_SUCCESS, "user": user.email}
