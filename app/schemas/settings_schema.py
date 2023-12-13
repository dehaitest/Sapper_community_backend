from pydantic import BaseModel
from typing import Optional

class SettingsBase(BaseModel):
    model: Optional[str] = None
    assistant_id: Optional[str] = None
    thread_id: Optional[str] = None
    instruction: Optional[str] = None
    file: Optional[str] = None
    tool: Optional[str] = None

    class Config:
        from_attributes = True

class SettingsCreate(SettingsBase):
    pass

class SettingsResponse(SettingsBase):
    id: int

class SettingsUpdate(SettingsBase):
    pass