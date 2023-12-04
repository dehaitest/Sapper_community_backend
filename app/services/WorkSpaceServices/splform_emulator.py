import json
from ..LLMs.assistant import Assistant
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class SPLEmulator:
    def __init__(self, client, assistant, thread) -> None:
        self.client = client
        self.assistant = assistant
        self.thread = thread

    @classmethod
    async def create(cls, db: AsyncSession, message_data):
        agent = await cls.get_agent_by_id(db, json.loads(message_data)['id'])
        try: 
            agent_settings = json.loads(agent.settings)
        except:
            agent_settings = {}
        agent_settings.update({'instruction': agent.spl})
        assistant_init = await Assistant.create()
        if 'assistant_id' in agent_settings and agent_settings.get('assistant_id'):
            assistant = await assistant_init.load_assistant(agent_settings)
            assistant = await assistant_init.update_assistant(agent_settings)
            print(assistant.tools)
        else:
            assistant = await assistant_init.create_assistant(agent_settings)
            agent_settings.update({'assistant_id': assistant.id})
        await cls.update_agent(db, agent.id, {'settings': json.dumps(agent_settings)})
        thread = await assistant_init.create_thread()
        return cls(assistant_init.client, assistant, thread)
    
    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent(db, agent_id, update_data)
    
    @staticmethod
    async def get_agent_by_id(db: AsyncSession, agent_id: int):
        agent = await select_agent_by_id(db, agent_id)
        return agent if agent else ''
    
    async def spl_emulator(self, message_data):
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message_data)

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