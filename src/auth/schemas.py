import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """UserModel used for view all user data"""
    uid: uuid.UUID
    username: str
    password: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    """UserCreateModel used for registration"""
    first_name: str = Field(max_length=16)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=16)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6, max_length=12)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Ronald",
                "last_name": "McDonald",
                "username": "mrbigmac",
                "email": "ronald.mcdonald@email.com",
                "password": "secret123"
            }
        }
    }


class UserLoginModel(BaseModel):
    """UserLoginModel used for login"""
    email: str = Field(max_length=40)
    password: str = Field(min_length=6, max_length=12)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "ronald.mcdonald@email.com",
                "password": "secret123"
            }
        }
    }
