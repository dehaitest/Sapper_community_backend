import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.config import settings

class SPLCompiler:
    def __init__(self, chatgpt_json, prompt_spl_compiler, instruction) -> None:
        self.prompt_spl_compiler = prompt_spl_compiler
        self.chatgpt_json = chatgpt_json
        self.instruction = instruction

    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_spl_compiler = await cls.get_prompt(db, 'spl_compiler')
        instruction = await cls.get_prompt(db, 'instruction')
        chatgpt_json = await Chatgpt_json.create()
        return cls(chatgpt_json, prompt_spl_compiler, instruction)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await select_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def get_agent_by_id(db: AsyncSession, agent_id: int):
        agent = await select_agent_by_id(db, agent_id)
        return agent if agent else ''

    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent(db, agent_id, update_data)

    async def update_settings(self, agent):
        try:
            agent_settings = json.loads(agent.settings) if agent.settings else {}
        except:
            agent_settings = {}
        agent_settings.update({'tools': [{"name": "retrieval", "detail": {"type": "retrieval"}, "active": 1}, {"name": "code_interpreter", "detail": {"type": "code_interpreter"}, "active": 1}]})
        agent_settings.update({'name': agent.name})
        agent_settings.update({'instruction': self.instruction})
        return agent_settings
    
    async def spl_compiler(self, db, agent_data):
        agent = await SPLCompiler.get_agent_by_id(db, json.loads(agent_data)['id'])
        prompt = [{"role": "system", "content": self.prompt_spl_compiler}]
        prompt.append({"role": "user", "content": "{}".format(agent.spl)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        default_settings = await self.update_settings(agent)
        new_agent_data = {'chain': json.dumps(result), 'settings': json.dumps(default_settings)}
        new_agent = await SPLCompiler.update_agent(db, json.loads(agent_data)['id'], new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"