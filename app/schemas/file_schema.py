# app/schemas/user_schema.py
from pydantic import BaseModel

class FileCreate(BaseModel):
    file_name: str
    file_id: str
    content_type: str

    class Config:
        from_attributes = True

class FileResponse(BaseModel):
    file_name: str
    file_id: str
    content_type: str
    active: int


