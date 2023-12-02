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
            user_settings = json.loads(agent.settings)
        except:
            user_settings = {}
        user_settings.update({'instruction': agent.spl})
        assistant_init = await Assistant.create()
        assistant = await assistant_init.create_assistant(user_settings)
        thread = await assistant_init.create_thread()
        return cls(assistant_init.client, assistant, thread)
    
    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int):
        agent = await select_agent_by_id(db, agent_id)
        return agent if agent else ''
    
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

        while True:
            # print('run status:', run.status)
            if run.status == "queued":
                break
            else:
                await asyncio.sleep(1)

        while True:
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id)
            # print('run status:', run.status)
            if run.status != "in_progress":
                break
            else:
                await asyncio.sleep(1)
        messages = await self.client.beta.threads.messages.list(thread_id=self.thread.id)
        # print(messages.data[0].content[0].text.value)
        yield messages.data[0].content[0].text.value