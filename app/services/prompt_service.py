from sqlalchemy.ext.asyncio import AsyncSession
from ..common import filter
from sqlalchemy.future import select
from ..models.prompt_model import Prompt
from typing import List

# Create prompt
async def create_prompt(db: AsyncSession, prompt_data: dict) -> Prompt:
    db_prompt = Prompt(**prompt_data, active=True)

    db.add(db_prompt)
    await db.commit()
    await db.refresh(db_prompt)
    return db_prompt

# Edit prompt
async def edit_prompt(db: AsyncSession, prompt_id: int, update_data: dict) -> Prompt:
    query = select(Prompt).where(Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()
    update_data = filter.filter_none_values(update_data)
    if db_prompt is not None:
        for key, value in update_data.items():
            setattr(db_prompt, key, value)
        await db.commit()
        await db.refresh(db_prompt)
        return db_prompt
    return None  

# Get prompt by name
async def get_prompt_by_name(db: AsyncSession, prompt_name: str) -> Prompt:
    result = await db.execute(select(Prompt).where(Prompt.name == prompt_name))
    return result.scalar_one_or_none()

# Get prompt by id
async def get_prompt_by_id(db: AsyncSession, prompt_id: int) -> Prompt:
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    return result.scalar()

# Delete prompt
async def delete_prompt(db: AsyncSession, prompt_id: int) -> bool:
    query = select(Prompt).where(Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()

    if db_prompt is not None:
        await db.delete(db_prompt)
        await db.commit()
        return True
    return False 

# Get all prompt
async def get_all_prompts(db: AsyncSession) -> List[Prompt]:
    result = await db.execute(select(Prompt))
    return result.scalars().all()


