import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_spl_to_splform

class NLToSPLForm:
    def __init__(self, prompt_nl2spl) -> None:
        self.prompt_nl2spl = prompt_nl2spl

    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_nl2spl = await cls.get_prompt(db, 'nl2spl')
        return cls(prompt_nl2spl)

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
    
    async def nl_to_splform(self, db, agent_data):
        new_nl = {'new_nl': json.loads(json.loads(agent_data)['nl'])['NL']}
        old_agent = await NLToSPLForm.get_agent_by_id(db, json.loads(agent_data)['id'])
        old_nl = {'old_nl': json.loads(old_agent.nl)['NL']}
        old_SPL = {'old_SPL': old_agent.spl}
        chatgpt_json = Chatgpt_json()
        prompt = [{"role": "system", "content": self.prompt_nl2spl}]
        prompt.append({"role": "user", "content": "[old_nl]: {}, [new_nl]: {}, [old_SPL]: {}".format(old_nl, new_nl, old_SPL)})
        response = await chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        splform = convert_spl_to_splform(result)
        new_agent_data = {'spl': json.dumps(result), 'spl_form': json.dumps(splform), 'nl': json.loads(agent_data)['nl']}
        new_agent = await NLToSPLForm.update_agent(db, json.loads(agent_data)['id'], new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"