import openai
from ...core.config import settings

class Chatbot():
    def __init__(self) -> None:
        openai.api_key = settings.OPENAI_KEY
        self.sysprompt = self.get_prompt()
        self.chat_history = self.assemble_chat_history()
        
    async def chat(self):
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            stream=True
        ):
#        self.chat_history.append({"role": response["choices"][0]["message"]["role"], "content": response["choices"][0]["message"]["content"]})
            yield response
    
    def get_prompt(self):
        return "You are a chatbot who has free chatting with me. Are you ready?"
    
    def assemble_chat_history(self):
        return [{"role": "system","content": self.sysprompt}]