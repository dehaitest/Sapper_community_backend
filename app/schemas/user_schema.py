# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr  
    password: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    uuid: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserWithToken(BaseModel):
    user: UserResponse
    token: Token
