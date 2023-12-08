from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SettingsBase(BaseModel):
    model: Optional[str] = None
    openai_key: Optional[str] = None
    assistant_id: Optional[str] = None
    instruction: Optional[str] = None
    file: Optional[str] = None
    tool: Optional[str] = None

    class Config:
        from_attributes = True

class SettingsCreate(SettingsBase):
    pass

class SettingsResponse(SettingsBase):
    pass

class SettingsUpdate(SettingsBase):
    pass