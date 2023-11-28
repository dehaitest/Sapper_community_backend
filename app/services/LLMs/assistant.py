import time
from openai import OpenAI 
from ...core.config import settings


class Assistant():
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_KEY) 