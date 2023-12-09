from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services import agent_service
from ....schemas.agent_schema import AgentCreate, AgentUpdate, AgentResponsePersonal, AgentResponseWorkspace, AgentResponse
from ...dependencies import get_current_user, auth_current_user
from typing import List

router = APIRouter()

# Create agent
@router.post("/agents/", response_model=AgentResponsePersonal)
async def create_agent_endpoint(agent_data: AgentCreate, db: AsyncSession = Depends(get_db_session), user_uuid = Depends(get_current_user)):
    return await agent_service.create_agent(db, user_uuid, agent_data.model_dump())

# Edit agent card
@router.put("/agents/card/{agent_uuid}", response_model=AgentResponsePersonal)
async def edit_agent_endpoint(agent_uuid: str, update_data: AgentCreate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agent = await agent_service.edit_agent(db, agent_uuid, update_data.model_dump())
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Edit agent 
@router.put("/agents/{agent_uuid}", response_model=AgentResponseWorkspace)
async def edit_agent_endpoint(agent_uuid: str, update_data: AgentUpdate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agent = await agent_service.edit_agent(db, agent_uuid, update_data.model_dump())
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Get agent by name
@router.get("/agents/by-name/", response_model=AgentResponsePersonal)
async def get_agent_by_name_endpoint(agent_name: str = Query(...), db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agent = await agent_service.get_agent_by_name(db, agent_name)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Get agent by UUID
@router.get("/agents/by-uuid/{agent_uuid}", response_model=AgentResponseWorkspace)
async def get_agent_by_uuid_endpoint(agent_uuid: str, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agent = await agent_service.get_agent_by_uuid(db, agent_uuid)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Get agents by creator
@router.get("/agents/by-creator/{user_uuid}", response_model=List[AgentResponsePersonal])
async def get_agents_by_creator_endpoint(user_uuid: str, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agents = await agent_service.get_agents_by_creator(db, user_uuid)
    if not agents:
        raise HTTPException(status_code=404, detail="Agents not found for the given creator")
    return agents

# Get agent by id
@router.get("/agents/by-id/{agent_id}", response_model=AgentResponsePersonal)
async def get_agent_by_id_endpoint(agent_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agent = await agent_service.get_agent_by_id(db, agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Delete agent by id
@router.delete("/agents/by-id/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_by_id_endpoint(agent_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    success = await agent_service.delete_agent_by_id(db, agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
# Delete agent by uuid
@router.delete("/agents/by-uuid/{agent_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_by_uuid_endpoint(agent_uuid: str, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    success = await agent_service.delete_agent_by_uuid(db, agent_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")

# Get all agents
@router.get("/agents/all", response_model=List[AgentResponse])
async def get_all_agents_endpoint(db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    agents = await agent_service.get_all_agents(db)
    return agents
