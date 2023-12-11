import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..user_service import get_user_by_uuid
from ..settings_service import get_settings_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.agent_schema import AgentResponseWorkspace

class SPLFormLint:
    def __init__(self, chatgpt_json, prompts, agent_uuid) -> None:
        self.prompts = prompts
        self.chatgpt_json = chatgpt_json
        self.agent_uuid = agent_uuid

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid):
        prompts = {
            'spl_linting': await cls.get_prompt(db, 'spl_linting'),
        }
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        chatgpt_settings = {'model': settings.model, 'openai_key': user.openai_key}
        chatgpt_json = await Chatgpt_json.create(chatgpt_settings)
        return cls(chatgpt_json, prompts, agent_uuid)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await get_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str):
        agent = await get_agent_by_uuid(db, agent_uuid)
        return agent if agent else ''
    
    @staticmethod
    async def get_settings_by_id(db: AsyncSession, id: int):
        return await get_settings_by_id(db, id)
    
    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''

    @staticmethod
    async def update_agent(db: AsyncSession, agent_uuid: str, update_data: dict):
        return await edit_agent_by_uuid(db, agent_uuid, update_data)
    
    async def splform_lint(self, db):
        agent = await SPLFormLint.get_agent_by_uuid(db, self.agent_uuid)
        spl = agent.spl
        prompt = [{"role": "system", "content": self.prompts.get('spl_linting')}]
        prompt.append({"role": "user", "content": "[SPL]: {}".format(spl)})
        print(prompt)
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        agent_data = {'lint': json.dumps(result)}
        agent = await SPLFormLint.update_agent(db, self.agent_uuid, agent_data)
        yield json.dumps(AgentResponseWorkspace.model_validate(agent, from_attributes=True).model_dump())
        yield "__END_OF_RESPONSE__"