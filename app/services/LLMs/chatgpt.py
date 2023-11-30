import openai
import asyncio
from ...core.config import settings

class Chatgpt:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY)

    async def process_message(self, message: list):
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=message,
                ),
                timeout=60  # Timeout in seconds
            )
            return response
        except asyncio.TimeoutError:
            print("Request timed out")
        except Exception as e:
            print(f"An error occurred: {e}")
    
class Chatgpt_json:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY)

    async def process_message(self, message: list):
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=message,
                    response_format={"type": "json_object"},
                ),
                timeout=60  # Timeout in seconds
            )
            return response
        except asyncio.TimeoutError:
            print("Request timed out")
        except Exception as e:
            print(f"An error occurred: {e}")


class Chatgpt_stream:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY)

    async def process_message(self, message: list):
        try:
            stream = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=message,
                    stream=True,
                ),
                timeout=60  # Timeout in seconds
            )
            async for part in stream:
                yield part
        except asyncio.TimeoutError:
            print("Request timed out")
        except Exception as e:
            print(f"An error occurred: {e}")