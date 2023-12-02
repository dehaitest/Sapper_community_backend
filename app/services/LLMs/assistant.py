import openai
from ...core.config import settings
import json

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

    async def load_assistant(self, user_settings: dict):
        try:
            assistant = await self.client.beta.assistants.retrieve(
                assistant_id=user_settings.get('assistant_id')
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when loading assistant: {e}")

    async def update_assistant(self, user_settings: dict):
        try:
            assistant = await self.client.beta.assistants.create(
                instructions=user_settings.get('instruction', ''),
                model=user_settings.get('model', settings.OPENAI_MODEL),
                name=user_settings.get('name', 'Assistant'),
                tools= [json.loads(json.loads(tool).get('detail')) for tool in user_settings.get('tools') if json.loads(tool).get('active')] if 'tool' in user_settings and user_settings['tools'] else [],
                file_ids=[json.loads(file).get('file_id') for file in user_settings.get('files') if json.loads(file).get('active')] if 'files' in user_settings and user_settings['files'] else [],
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when creating assistant: {e}")

    async def create_thread(self):
        try:
            return await self.client.beta.threads.create()
        except Exception as e:
            print(f"An error occurred when creating thread: {e}")
