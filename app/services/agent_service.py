from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ..models.agent_model import Agent
from ..common import id_generation, data_conversion
from ..services import settings_service
import json

# Create Agent
async def create_agent(db: AsyncSession, user_uuid: str, agent_data: dict) -> Agent:
    uuid = 'agent_{}'.format(id_generation.generate_id())
    while await get_agent_by_uuid(db, uuid):
        uuid = 'agent_{}'.format(id_generation.generate_id())
    settings = await settings_service.create_settings(db, {})
    db_agent = Agent(**agent_data, uuid=uuid, owner_uuid=user_uuid, creator_uuid=user_uuid, settings_id=settings.id, active=True)
    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    return db_agent

# Edit Agent by UUID
async def edit_agent_by_uuid(db: AsyncSession, agent_uuid: str, update_data: dict) -> Agent:
    query = select(Agent).where(Agent.uuid == agent_uuid)
    result = await db.execute(query)
    db_agent = result.scalar_one_or_none()
    if db_agent is not None:
        for key, value in update_data.items():
            if key == 'spl_form':
                spl = data_conversion.convert_splform_to_spl(json.loads(value))
                setattr(db_agent, 'spl', json.dumps(spl))
            setattr(db_agent, key, value)
        await db.commit()
        await db.refresh(db_agent)
        return db_agent
    return None  

# Get Agent by Name
async def get_agents_by_name(db: AsyncSession, agent_name: str) -> List[Agent]:
    result = await db.execute(select(Agent).where(Agent.name == agent_name))
    return result.scalars().all()

# Get Agent by Creator
async def get_agents_by_creator(db: AsyncSession, creator_uuid: str) -> List[Agent]:
    result = await db.execute(select(Agent).where(Agent.creator_uuid == creator_uuid))
    return result.scalars().all()

# Get Agent by ID
async def get_agent_by_id(db: AsyncSession, agent_id: int) -> Agent:
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    return result.scalar_one_or_none()

# Get Agent by UUID
async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str) -> Agent:
    result = await db.execute(select(Agent).where(Agent.uuid == agent_uuid))
    return result.scalar_one_or_none()

# Delete Agent by ID
async def delete_agent_by_id(db: AsyncSession, agent_id: int) -> bool:
    query = select(Agent).where(Agent.id == agent_id)
    result = await db.execute(query)
    db_agent = result.scalar_one_or_none()
    if db_agent is not None:
        await db.delete(db_agent)
        await db.commit()
        return True
    return False 

# Delete Agent by UUID
async def delete_agent_by_uuid(db: AsyncSession, agent_uuid: str) -> bool:
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
