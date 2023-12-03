import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_splform_to_spl

class SPLFormToNL:
    def __init__(self, chatgpt_json, prompt_spl2nl) -> None:
        self.prompt_spl2nl = prompt_spl2nl
        self.chatgpt_json = chatgpt_json

    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_spl2nl = await cls.get_prompt(db, 'spl2nl')
        chatgpt_json = await Chatgpt_json.create()
        return cls(chatgpt_json, prompt_spl2nl)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await select_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def get_splform_by_id(db: AsyncSession, agent_id: int):
        agent = await select_agent_by_id(db, agent_id)
        return agent.spl_form if agent else ''

    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent(db, agent_id, update_data)
    
    async def splform_to_nl(self, db, agent_data):
        splform = json.loads(json.loads(agent_data)['spl_form'])
        spl = convert_splform_to_spl(splform)
        prompt = [{"role": "system", "content": self.prompt_spl2nl}]
        prompt.append({"role": "user", "content": "[SPL]: {}".format(spl)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        new_agent_data = {'spl': json.dumps(spl), 'spl_form': json.dumps(splform), 'nl': json.dumps(result)}
        new_agent = await SPLFormToNL.update_agent(db, int(json.loads(agent_data)['id']), new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"