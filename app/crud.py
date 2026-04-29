from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash
from app.models import User as UserModel


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
