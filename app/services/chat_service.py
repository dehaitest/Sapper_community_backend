from .LLMs.Chatbot import Chatbot
import asyncio

class ChatService:
    def __init__(self) -> None:
        self.chatbot = Chatbot()

    async def process_message(self, message: str):
        message = [{"role": "user", "content": message}]
        self.chatbot.chat_history = self.chatbot.chat_history + message
        history = ''
        async for part in self.chatbot.chat():
            if part.choices[0].finish_reason == "stop":
                self.chatbot.chat_history.append({"role": "assistant", "content": history})
                yield "__END_OF_RESPONSE__"  # Special marker indicating end of response
                break
            history += part.choices[0].delta.content
            await asyncio.sleep(0.001)
            yield part.choices[0].delta.content
