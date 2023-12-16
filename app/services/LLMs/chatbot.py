import openai
import asyncio
from ...core.config import settings

class Chatbot():
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY) 
        self.sysprompt = self.get_prompt()
        self.chat_history = self.assemble_chat_history()

    async def chat(self):
        try:
            stream = await asyncio.wait_for(
                self.client.chat.completions.create(
                    # model=settings.OPENAI_MODEL,
                    model="gpt-4-1106-preview",
                    messages=self.chat_history,
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
    
    def get_prompt(self):
        return "You are a chatbot who has free chatting with me. Are you ready?"
    
    def assemble_chat_history(self):
        return [{"role": "system", "content": self.sysprompt}]
