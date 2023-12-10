# app/api/v1/endpoints/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ....services import user_service
from ....services.database import get_db_session
from ....schemas.user_schema import UserCreate, UserResponse, UserWithToken, Token, UserUpdate
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from ...dependencies import auth_current_user

router = APIRouter()

# Create user / Sign up
@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    existing_user = await user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email address is already in use."
        )
    return await user_service.create_user(db, user.model_dump())

# Get user by ID
@router.get("/users/by-id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    db_user = await user_service.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get user by UUID
@router.get("/users/by-uuid/{user_uuid}", response_model=UserResponse)
async def get_user_by_uuid(user_uuid: str, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    db_user = await user_service.get_user_by_uuid(db, user_uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Edit user by UUID
@router.put("/users/by-uuid/{user_uuid}", response_model=UserResponse)
async def edit_user_by_uuid_endpoint(user_uuid: str, update_data: UserUpdate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    user = await user_service.edit_user_by_uuid(db, user_uuid, update_data.model_dump())
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Login
@router.post("/users/login", response_model=UserWithToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    # Authenticate user
    user = await user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_service.edit_user_by_id(db, user.id, {"last_login": datetime.utcnow()})
    access_token = user_service.create_access_token(data={"sub": user.uuid})
    refresh_token = user_service.create_refresh_token(data={"sub": user.uuid})
    
    user_response = UserResponse(uuid=user.uuid, name=user.name, active=user.active)
    token_data = Token(access_token=access_token)
    response_data = UserWithToken(user=user_response, token=token_data)
    response = JSONResponse(content=response_data.model_dump())
    max_age = 30 * 24 * 60 * 60  # 30 days, in seconds
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=max_age, samesite='None', secure=True)
    return response

@router.post("/users/refreshtoken", response_model=Token)
async def refresh_access_token(refresh_token: Optional[str] = Cookie(None), db: AsyncSession = Depends(get_db_session)):
    if refresh_token is None or not (uuid := await user_service.validate_token(db, refresh_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    access_token = user_service.create_access_token(data={"sub": uuid})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
