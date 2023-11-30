from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services.agent_service import create_agent, edit_agent, select_agent_by_name, delete_agent, get_all_agents, select_agent_by_id
from ....schemas.agent_schema import AgentCreate, AgentUpdate, AgentResponse
from typing import List

router = APIRouter()

# Create agent
@router.post("/agents/", response_model=AgentResponse)
async def create_agent_endpoint(agent_data: AgentCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_agent(db, agent_data.dict())

# Edit agent
@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def edit_agent_endpoint(agent_id: int, update_data: AgentUpdate, db: AsyncSession = Depends(get_db_session)):
    agent = await edit_agent(db, agent_id, update_data.dict())
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Get agent by name
@router.get("/agents/by-name/", response_model=AgentResponse)
async def get_agent_by_name_endpoint(agent_name: str, db: AsyncSession = Depends(get_db_session)):
    agent = await select_agent_by_name(db, agent_name)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Get agent by id
@router.get("/agents/by-id/{agent_id}", response_model=AgentResponse)
async def get_agent_by_id_endpoint(agent_id: int, db: AsyncSession = Depends(get_db_session)):
    agent = await select_agent_by_id(db, agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Delete agent
@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_endpoint(agent_id: int, db: AsyncSession = Depends(get_db_session)):
    success = await delete_agent(db, agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")

# Get all agents
@router.get("/agents/all", response_model=List[AgentResponse])
async def get_all_agents_endpoint(db: AsyncSession = Depends(get_db_session)):
    agents = await get_all_agents(db)
    return agents
