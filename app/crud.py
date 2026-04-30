from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import get_password_hash, verify_password
from app.models import User as UserModel
from app.schemas import LoginSchema, UserUpdate


class UserCRUD:
    @staticmethod
    def not_found_user(user: UserModel | None = None):
        if not user:
            raise UserNotFoundError()

    @staticmethod
    def create_user(db: Session, email: str, password: str, full_name: str):

        user_db = UserCRUD.get_user_by_email(
            db=db, email=email, should_seek_user=False, active_only=False
        )

        if user_db:
            raise UserAlreadyExistsError()

        new_user = UserModel(
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate):
        user = UserCRUD.get_user_by_id(db=db, user_id=user_id)

        update_data = user_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "password":
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserCRUD.get_user_by_id(db=db, user_id=user_id)

        setattr(user, "is_active", False)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_all_users(db: Session, active_only: bool = True) -> List[UserModel]:
        query = db.query(UserModel)

        if active_only:
            query = query.filter(UserModel.is_active)

        users = query.all()
        return users

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        UserCRUD.not_found_user(user=user)

        return user

    @staticmethod
    def get_user_by_email(
        db: Session, email: str, active_only: bool = True, should_seek_user: bool = True
    ):
        query = db.query(UserModel).filter(UserModel.email == email)

        if active_only:
            query = query.filter(UserModel.is_active)

        user = query.first()

        if should_seek_user:
            UserCRUD.not_found_user(user=user)

        return user

    @staticmethod
    def is_user_authenticated(db: Session, data: LoginSchema):
        user = (
            db.query(UserModel)
            .filter(UserModel.email == data.email, UserModel.is_active)
            .first()
        )

        if not user or not verify_password(
            plain_password=data.password, hashed_password=user.hashed_password
        ):
            raise InvalidCredentialsError()

        return user
