# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr  
    password: str

class UserResponse(BaseModel):
    uuid: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserWithToken(BaseModel):
    user: UserResponse
    token: Token

    class Config:
        from_attributes = True
