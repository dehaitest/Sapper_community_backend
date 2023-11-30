from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from ..models.prompt_model import Prompt
from typing import List

async def create_prompt(db: AsyncSession, prompt_data: dict) -> Prompt:
    db_prompt = Prompt(
        name=prompt_data['name'],
        prompt=prompt_data['prompt'],
        description=prompt_data.get('description', ''),  # Using .get() for optional fields
        create_datetime=prompt_data.get('create_datetime', datetime.utcnow()),
        update_datetime=prompt_data.get('update_datetime', datetime.utcnow()),
        active=prompt_data.get('active', True)  # Default to True if not provided
    )

    db.add(db_prompt)
    await db.commit()
    await db.refresh(db_prompt)
    return db_prompt

async def edit_prompt(db: AsyncSession, prompt_id: int, update_data: dict) -> Prompt:
    query = select(Prompt).where(Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()

    if db_prompt is not None:
        for key, value in update_data.items():
            setattr(db_prompt, key, value)
        await db.commit()
        await db.refresh(db_prompt)
        return db_prompt

    return None  

async def select_prompt_by_name(db: AsyncSession, prompt_name: str) -> Prompt:
    result = await db.execute(select(Prompt).where(Prompt.name == prompt_name))
    return result.scalar_one_or_none()

async def select_prompt_by_id(db: AsyncSession, prompt_id: int) -> Prompt:
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    return result.scalar()

async def delete_prompt(db: AsyncSession, prompt_id: int) -> bool:
    query = select(Prompt).where(Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()

    if db_prompt is not None:
        await db.delete(db_prompt)
        await db.commit()
        return True

    return False 

async def get_all_prompts(db: AsyncSession) -> List[Prompt]:
    result = await db.execute(select(Prompt))
    return result.scalars().all()


