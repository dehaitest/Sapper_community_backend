from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base model for shared attributes
class AgentBase(BaseModel):
    name: str
    image: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    nl: Optional[str] = None
    created_by: Optional[str] = None

# Model for creation requests
class AgentCreate(AgentBase):
    pass

# Model for update requests
class AgentUpdate(AgentBase):
    pass

# Model for response, including database-generated attributes
class AgentResponse(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    spl: Optional[str] = None
    spl_form: Optional[str] = None
    nl: Optional[str] = None
    created_by: Optional[str] = None
    create_datetime: datetime
    update_datetime: datetime
    active: bool

    class Config:
        from_attributes = True
