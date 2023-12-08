# app/models/settings_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    agent_uuid = Column(String(32))
    model = Column(String(255))
    assistant_id = Column(String(64))
    instruction = Column(Text)
    file = Column(Text)
    tool = Column(Text)
    create_datetime = Column(DateTime, default=datetime.utcnow)
    update_datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
