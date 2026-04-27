from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: Annotated[EmailStr, Field(description="User Email")]
    full_name: Annotated[str, Field(min_length=3, max_length=50)]


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=3, max_length=128)]


class User(UserBase):
    id: int

    model_config = {"from_attributes": True}
