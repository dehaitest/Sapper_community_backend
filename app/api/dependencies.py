from fastapi import Header, HTTPException, status, Depends
from ..services.user_service import validate_token 
from ..services.database import get_db_session 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)) -> str:
    email = await validate_token(db, token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return email

async def auth_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)) -> str:
    email = await validate_token(db, token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
