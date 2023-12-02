import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_splform_to_spl

class SPLCompiler:
    def __init__(self, prompt_spl_compiler) -> None:
        self.prompt_spl_compiler = prompt_spl_compiler

    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_spl_compiler = await cls.get_prompt(db, 'spl_compiler')
        return cls(prompt_spl_compiler)

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
    
    async def spl_compiler(self, db, agent_data):
        agent = await SPLCompiler.get_agent_by_id(db, json.loads(agent_data)['id'])
        chatgpt_json = Chatgpt_json()
        prompt = [{"role": "system", "content": self.prompt_spl_compiler}]
        prompt.append({"role": "user", "content": "{}".format(agent.spl)})
        response = await chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        new_agent_data = {'chain': json.dumps(result)}
        new_agent = await SPLCompiler.update_agent(db, json.loads(agent_data)['id'], new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"