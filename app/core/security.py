import bcrypt

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from app.database import DbDep
from app.core.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {"sub": str(user_id), "exp": expire, "iat": datetime.now()}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")

        if user_id is None:
            raise UnauthorizedError()
        return user_id
    except JWTError:
        raise UnauthorizedError()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbDep):

    from app.crud import UserCRUD

    user_id = decode_token(token=token)

    user = UserCRUD.get_user_by_id(db=db, user_id=int(user_id))

    return user


async def list_users(token: Annotated[str, Depends(oauth2_scheme)], db: DbDep):

    from app.crud import UserCRUD

    decode_token(token=token)

    users = UserCRUD.get_all_users(db=db)

    return users
