import openai
from ...core.config import settings

class Chatgpt():
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY) 

    async def process_message(self, message: list):
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=message,
        )
        return response
    
class Chatgpt_json():
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY) 

    async def process_message(self, message: list):
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=message,
            response_format={ "type": "json_object" },
        )
        return response
    
class Chatgpt_strem():
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY) 

    async def process_message(self, message: list):
        stream = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=message,
            stream=True,
        )
        async for part in stream:
            yield part
        
