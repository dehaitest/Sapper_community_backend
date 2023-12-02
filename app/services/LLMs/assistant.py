import openai
from ...core.config import settings

class Assistant:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls):
        instance = cls()
        await instance.async_init()
        return instance

    async def async_init(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_KEY)

    async def create_assistant(self, user_settings: dict):
        try:
            assistant = await self.client.beta.assistants.create(
                instructions=user_settings.get('instruction', ''),
                model=settings.OPENAI_MODEL,
                name=user_settings.get('name', 'Assistant'),
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when creating assistant: {e}")

    async def create_thread(self):
        try:
            return await self.client.beta.threads.create()
        except Exception as e:
            print(f"An error occurred when creating thread: {e}")
