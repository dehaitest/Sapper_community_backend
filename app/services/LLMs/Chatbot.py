import openai
from ...core.config import settings

class Chatbot():
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY) 
        self.sysprompt = self.get_prompt()
        self.chat_history = self.assemble_chat_history()
        
    async def chat(self):
        stream = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.chat_history,
            stream=True,
        )
        async for part in stream:
            yield part
    
    def get_prompt(self):
        return "You are a chatbot who has free chatting with me. Are you ready?"
    
    def assemble_chat_history(self):
        return [{"role": "system", "content": self.sysprompt}]
