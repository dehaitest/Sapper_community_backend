import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import select_agent_by_id, edit_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_spl_to_splform

class SPLFormCopilot:
    def __init__(self, chatgpt_json, prompt_splform_copilot) -> None:
        self.prompt_splform_copilot = prompt_splform_copilot
        self.chatgpt_json = chatgpt_json

    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_splform_copilot = await cls.get_prompt(db, 'splform_copilot')
        chatgpt_json = await Chatgpt_json.create()
        return cls(chatgpt_json, prompt_splform_copilot)

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
    
    async def splform_copilot(self, db, message_data):
        old_agent = await SPLFormCopilot.get_agent_by_id(db, json.loads(message_data)['id'])
        print('old_agent', old_agent)
        old_SPL = {'old_SPL': old_agent.spl}
        prompt = [{"role": "system", "content": self.prompt_splform_copilot}]
        prompt.append({"role": "user", "content": "[user description]: {}, [old_SPL]: {}".format(json.loads(message_data)['message'], old_SPL)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        splform = convert_spl_to_splform(result)
        new_agent_data = {'spl': json.dumps(result), 'spl_form': json.dumps(splform)}
        new_agent = await SPLFormCopilot.update_agent(db, json.loads(message_data)['id'], new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"