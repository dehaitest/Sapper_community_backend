from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from typing import List
from ..models.agent_model import Agent


# Create Agent
async def create_agent(db: AsyncSession, agent_data: dict) -> Agent:
    db_agent = Agent(
        **agent_data,
        create_datetime=datetime.utcnow(),
        update_datetime=datetime.utcnow(),
        active=True
    )

    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    return db_agent

# Edit Agent
async def edit_agent(db: AsyncSession, agent_uuid: str, update_data: dict) -> Agent:
    query = select(Agent).where(Agent.uuid == agent_uuid)
    result = await db.execute(query)
    db_agent = result.scalar_one_or_none()

    if db_agent is not None:
        for key, value in update_data.items():
            setattr(db_agent, key, value)
        await db.commit()
        await db.refresh(db_agent)
        return db_agent

    return None  

# Select Agent by Name
async def select_agents_by_name(db: AsyncSession, agent_name: str) -> List[Agent]:
    result = await db.execute(select(Agent).where(Agent.name == agent_name))
    return result.scalars().all()

# Select Agent by Creator
async def select_agents_by_creator(db: AsyncSession, creator_id: int) -> List[Agent]:
    result = await db.execute(select(Agent).where(Agent.creator_id == creator_id))
    return result.scalars().all()

# Select Agent by ID
async def select_agent_by_id(db: AsyncSession, agent_id: int) -> Agent:
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    return result.scalar_one_or_none()

# Select Agent by UUID
async def select_agent_by_uuid(db: AsyncSession, agent_uuid: str) -> Agent:
    result = await db.execute(select(Agent).where(Agent.uuid == agent_uuid))
    return result.scalar_one_or_none()

# Delete Agent
async def delete_agent(db: AsyncSession, agent_uuid: str) -> bool:
    query = select(Agent).where(Agent.uuid == agent_uuid)
    result = await db.execute(query)
    db_agent = result.scalar_one_or_none()

    if db_agent is not None:
        await db.delete(db_agent)
        await db.commit()
        return True

    return False 

# Get All Agents
async def get_all_agents(db: AsyncSession) -> List[Agent]:
    result = await db.execute(select(Agent))
    return result.scalars().all()
