from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from ..models.settings_model import Settings
from typing import List

# Create settings
async def create_settings(db: AsyncSession, settings_data: dict) -> Settings:
    db_settings = Settings(**settings_data)

    db.add(db_settings)
    await db.commit()
    await db.refresh(db_settings)
    return db_settings

# Edit settings
async def edit_settings(db: AsyncSession, settings_id: int, update_data: dict) -> Settings:
    query = select(Settings).where(Settings.id == settings_id)
    result = await db.execute(query)
    db_settings = result.scalar_one_or_none()

    if db_settings is not None:
        for key, value in update_data.items():
            setattr(db_settings, key, value)
        await db.commit()
        await db.refresh(db_settings)
        return db_settings
    return None  

# Get settings by id
async def get_settings_by_id(db: AsyncSession, settings_id: int) -> Settings:
    result = await db.execute(select(Settings).where(Settings.id == settings_id))
    return result.scalar_one()

# Delete settings
async def delete_settings(db: AsyncSession, settings_id: int) -> bool:
    query = select(Settings).where(Settings.id == settings_id)
    result = await db.execute(query)
    db_settings = result.scalar_one_or_none()

    if db_settings is not None:
        await db.delete(db_settings)
        await db.commit()
        return True
    return False 

# Get all settings
async def get_all_settings(db: AsyncSession) -> List[Settings]:
    result = await db.execute(select(Settings))
    return result.scalars().all()