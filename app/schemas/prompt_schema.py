from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base model for shared attributes
class PromptBase(BaseModel):
    name: str
    prompt: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Model for creation requests
class PromptCreate(PromptBase):
    pass

# Model for update requests
class PromptUpdate(PromptBase):
    pass

# Model for response, including database-generated attributes
class PromptResponse(BaseModel):
    id: int
    name: str
    prompt: str
    description: Optional[str] = None
    create_datetime: datetime
    update_datetime: datetime
    active: bool
