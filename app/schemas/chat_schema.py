# app/schemas/chat_schema.py

from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str
