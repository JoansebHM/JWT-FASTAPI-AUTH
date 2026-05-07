from typing import Annotated, List

from app.dependencies import DbDep
from app.crud import UserCRUD
from app.schemas import User as UserSchema, UserUpdate
from app.models import User as UserModel

from fastapi import Depends, APIRouter
from app.core.security import list_users, get_current_user


router = APIRouter()


@router.get("/users", response_model=List[UserSchema])
async def find_all(users: Annotated[List[UserModel], Depends(list_users)]):
    return users


@router.get("/users/me", response_model=UserSchema)
async def find_me(user: Annotated[UserModel, Depends(get_current_user)]):
    return user


@router.get("/users/{user_id}", response_model=UserSchema)
async def find_one(user_id: int, db: DbDep):
    return UserCRUD.get_user_by_id(db=db, user_id=user_id)


@router.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: DbDep):
    return UserCRUD.update_user(db=db, user_id=user_id, user_update=user_update)


@router.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: DbDep):
    return UserCRUD.delete_user(db=db, user_id=user_id)
