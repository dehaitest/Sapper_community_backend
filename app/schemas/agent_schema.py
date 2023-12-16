from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base model for shared attributes
class AgentBase(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    cfp: Optional[str] = None
    lint: Optional[str] = None
    chain: Optional[str] = None
    settings_id: Optional[int] = None
    owner_uuid: Optional[str] = None
    creator_uuid: Optional[str] = None
    active: Optional[bool] = None

    class Config:
        from_attributes = True

class AgentDefault(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    cfp: Optional[str] = None
    lint: Optional[str] = None
    chain: Optional[str] = None

    class Config:
        from_attributes = True

# Model for creation requests
class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Model for update requests
class AgentUpdate(AgentBase):
    pass

# Model for response, including database-generated attributes
class AgentResponseWorkspace(BaseModel):
    uuid: str
    name: str
    image: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    cfp: Optional[str] = None
    lint: Optional[str] = None
    chain: Optional[str] = None
    settings_id: int

class AgentResponsePersonal(BaseModel):
    uuid: str
    name: str
    image: Optional[str] = None
    owner_uuid: str
    creator_uuid: str
    settings_id: int
    create_datetime: datetime
    update_datetime: datetime
    active: bool

class AgentResponse(BaseModel):
    id: int
    uuid: str
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    cfp: Optional[str] = None
    lint: Optional[str] = None
    chain: Optional[str] = None
    settings_id: Optional[int] = None
    owner_uuid: Optional[str] = None
    creator_uuid: Optional[str] = None
    active: Optional[bool] = None