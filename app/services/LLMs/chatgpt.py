import openai
import asyncio
from fastapi import HTTPException, status

class Chatgpt:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls, settings):
        instance = cls()
        await instance.async_init(settings)
        return instance

    async def async_init(self, settings):
        self.client = openai.AsyncOpenAI(api_key=settings.get('openai_key'))
        self.model = settings.get('model')

    async def process_message(self, message: list):
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=message,
                ),
                timeout=120  # Timeout in seconds
            )
            return response
        except asyncio.TimeoutError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request timed out")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"An error occurred: {e}")
    
class Chatgpt_json:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls, settings):
        instance = cls()
        await instance.async_init(settings)
        return instance

    async def async_init(self, settings):
        self.client = openai.AsyncOpenAI(api_key=settings.get('openai_key'))
        self.model = settings.get('model')

    async def process_message(self, message: list):
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=message,
                    response_format={"type": "json_object"},
                ),
                timeout=120  # Timeout in seconds
            )
            return response
        except asyncio.TimeoutError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request timed out")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"An error occurred: {e}")


class Chatgpt_stream:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls, settings):
        instance = cls()
        await instance.async_init(settings)
        return instance

    async def async_init(self, settings):
        self.client = openai.AsyncOpenAI(api_key=settings.get('openai_key'))
        self.model = settings.get('model')

    async def process_message(self, message: list):
        try:
            stream = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=message,
                    stream=True,
                ),
                timeout=120  # Timeout in seconds
            )
            async for part in stream:
                yield part
        except asyncio.TimeoutError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request timed out")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"An error occurred: {e}")
