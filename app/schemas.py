from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.models import UserTypes


class UserBase(BaseModel):
    email: Annotated[EmailStr | None, Field(description="User Email")] = None
    full_name: Annotated[str | None, Field(min_length=3, max_length=50)] = None


class UserCreate(UserBase):
    email: Annotated[EmailStr, Field(description="User Email")]
    password: Annotated[str, Field(min_length=3, max_length=128)]


class UserUpdate(UserBase):
    password: Annotated[str | None, Field(min_length=3, max_length=128)] = None


class LoginSchema(BaseModel):
    email: Annotated[EmailStr, Field(description="User Email")]
    password: Annotated[str, Field(min_length=3, max_length=50)]


class User(UserBase):
    id: int
    is_active: bool
    user_type: UserTypes

    model_config = {"from_attributes": True}
