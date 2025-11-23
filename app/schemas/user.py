from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class UserOptionalFields(BaseModel):
    first_name: str | None = Field(None, max_length=100, examples=["Jan"])
    last_name: str | None = Field(None, max_length=100, examples=["Kowalski"])
    bio: str | None = Field(
        None, max_length=500, examples=["I love teaching programming."]
    )
    avatar_url: str | None = Field(
        None, max_length=255, examples=["https://cdn.site.com/avatar.jpg"]
    )


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=80, examples=["JanKowalski"])
    email: EmailStr = Field(..., examples=["jan.kowalski@example.com"])
    role: UserRole = Field(
        default=UserRole.STUDENT,
        examples=[UserRole.STUDENT],
    )


class UserCreate(UserBase, UserOptionalFields):
    auth0_id: str = Field(..., max_length=255, examples=["auth0|1234567890abcdef"])


class UserUpdate(UserOptionalFields):
    username: str | None = Field(None, min_length=3, max_length=80)
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserInDB(UserBase):
    id: int = Field(..., examples=[1])
    auth0_id: str = Field(..., examples=["auth0|1234567890abcdef"])
    is_active: bool = Field(..., examples=[True])
    created_at: datetime = Field(...)
    updated_at: datetime | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserInDB):
    pass
