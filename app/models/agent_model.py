# app/models/agent_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = 'agent'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(32), unique=True, index=True)
    name = Column(String(32))
    image = Column(String(255))
    description = Column(Text)
    spl = Column(Text)
    spl_form = Column(Text)
    cfp = Column(Text)
    lint = Column(Text)
    chain = Column(Text)
    settings_id = Column(Integer)
    owner_uuid = Column(String(32))
    creator_uuid = Column(String(32))
    create_datetime = Column(DateTime, default=datetime.utcnow)
    update_datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean)