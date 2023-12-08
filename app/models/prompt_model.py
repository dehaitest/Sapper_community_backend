# app/models/prompt_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompt'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    prompt = Column(Text)
    description = Column(Text)
    create_datetime = Column(DateTime, default=datetime.utcnow)
    update_datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean)