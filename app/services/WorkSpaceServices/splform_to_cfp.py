import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..settings_service import get_settings_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_splform_to_spl

class SPLFormToCFP:
    def __init__(self, chatgpt_json, prompts, agent_uuid) -> None:
        self.prompts = prompts
        self.chatgpt_json = chatgpt_json
        self.agent_uuid = agent_uuid

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid: str):
        prompts = {
            'generate_cfp': await cls.get_prompt(db, 'generate_cfp'),
            'cfp_debug': await cls.get_prompt(db, 'cfp_debug'),
        }
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        chatgpt_json = await Chatgpt_json.create(settings)
        return cls(chatgpt_json, prompts, agent_uuid)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await get_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def get_settings_by_id(db: AsyncSession, id: int):
        return await get_settings_by_id(db, id)
    
    @staticmethod
    async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str):
        agent = await get_agent_by_uuid(db, agent_uuid)
        return agent if agent else ''

    @staticmethod
    async def update_agent(db: AsyncSession, agent_uuid: str, update_data: dict):
        return await edit_agent_by_uuid(db, agent_uuid, update_data)
    
    async def splform_to_cfp(self, db, agent_data):
        splform = json.loads(json.loads(agent_data)['spl_form'])
        spl = convert_splform_to_spl(splform)
        prompt = [{"role": "system", "content": self.prompt_spl2nl}]
        prompt.append({"role": "user", "content": "[SPL]: {}".format(spl)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        new_agent_data = {'spl': json.dumps(spl), 'spl_form': json.dumps(splform), 'nl': json.dumps(result)}
        new_agent = await SPLFormToCFP.update_agent(db, self.agent_uuid, new_agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"