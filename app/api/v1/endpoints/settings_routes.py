from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services import settings_service
from ....schemas.settings_schema import SettingsCreate, SettingsUpdate, SettingsResponse
from ...dependencies import auth_current_user
from typing import List

router = APIRouter()

# Create settings
@router.post("/settings/", response_model=SettingsResponse)
async def create_settings_endpoint(settings_data: SettingsCreate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    return await settings_service.create_settings(db, settings_data.model_dump())

# Edit settings
@router.put("/settings/{settings_id}", response_model=SettingsResponse)
async def edit_settings_endpoint(settings_id: int, update_data: SettingsUpdate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    settings = await settings_service.edit_settings(db, settings_id, update_data.model_dump())
    if settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

# Get settings by id
@router.get("/settings/by-id/{settings_id}", response_model=SettingsResponse)
async def get_settings_by_id_endpoint(settings_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    settings = await settings_service.get_settings_by_id(db, settings_id)
    if settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

# Delete settings
@router.delete("/settings/{settings_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_settings_endpoint(settings_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    success = await settings_service.delete_settings(db, settings_id)
    if not success:
        raise HTTPException(status_code=404, detail="Settings not found")

# Get all settings
@router.get("/settings/all", response_model=List[SettingsResponse])
async def get_all_settings_endpoint(db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    settings = await settings_service.get_all_settings(db)
    return settings
