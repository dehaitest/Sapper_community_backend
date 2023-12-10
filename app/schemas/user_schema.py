# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr  
    password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    openai_key: Optional[str] = None
    active: Optional[bool] = None

class UserResponse(BaseModel):
    uuid: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    openai_key: Optional[str] = None
    active: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserWithToken(BaseModel):
    user: UserResponse
    token: Token
