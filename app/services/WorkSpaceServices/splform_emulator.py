import json
from ..LLMs.assistant import Assistant
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..settings_service import get_settings_by_id, edit_settings
from ..user_service import get_user_by_uuid
from ...schemas.settings_schema import SettingsResponse
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class SPLEmulator:
    def __init__(self, client, assistant, thread) -> None:
        self.client = client
        self.assistant = assistant
        self.thread = thread

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid):
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        settings = SettingsResponse.model_validate(settings, from_attributes=True).model_dump()
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        assistant_init = await Assistant.create({'openai_key': user.openai_key})
        settings.update({'instruction': agent.spl})
        if settings.get('assistant_id', ''):
            assistant = await assistant_init.load_assistant(settings)
            assistant = await assistant_init.update_assistant(settings)
        else:
            assistant = await assistant_init.create_assistant(settings)
            settings.update({'assistant_id': assistant.id})
        await cls.update_settings(db, agent.settings_id, settings)
        thread = await assistant_init.create_thread()
        return cls(assistant_init.client, assistant, thread)
    
    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent_by_uuid(db, agent_id, update_data)
    
    @staticmethod
    async def get_settings_by_id(db: AsyncSession, id: int):
        return await get_settings_by_id(db, id)
    
    @staticmethod
    async def update_settings(db: AsyncSession, settings_id: int, update_data: dict):
        return await edit_settings(db, settings_id, update_data)
    
    @staticmethod
    async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str):
        agent = await get_agent_by_uuid(db, agent_uuid)
        return agent if agent else ''

    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''    

    async def spl_emulator(self, message_data):
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=json.loads(message_data).get('message'),
            file_ids=json.loads(message_data).get('file_ids', [])
            )

        run = await self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id)

        while run.status == "queued":
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id)

        while run.status == "in_progress":
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id)
        
        messages = await self.client.beta.threads.messages.list(thread_id=self.thread.id)
        yield messages.data[0].content[0].text.value