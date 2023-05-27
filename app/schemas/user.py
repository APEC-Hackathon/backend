from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_superuser: bool = False
    prefered_language: Optional[str] = None
    organization_name: Optional[str] = None
    organization_description: Optional[str] = None
    organization_rating: Optional[float] = None
    country: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    prefered_language: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass 


class UserInDB(UserInDBBase):
    hashed_password: str
    