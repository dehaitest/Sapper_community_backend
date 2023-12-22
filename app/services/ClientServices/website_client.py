import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..settings_service import get_settings_by_id
from ..user_service import get_user_by_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.agent_schema import AgentResponseWorkspace

class WebsiteClient:
    def __init__(self, chatgpt_json, prompts, agent_uuid) -> None:
        self.prompts = prompts
        self.chatgpt_json = chatgpt_json
        self.agent_uuid = agent_uuid

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid, instruction):
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        instruction_content = json.loads(agent.spl).get(instruction)
        persona_content = json.loads(agent.spl).get('Persona')
        audience_content = json.loads(agent.spl).get('Audience')
        prompts = {
            "system": "Persona: {}\nAudience: {}\nInstruction:{}".format(persona_content, audience_content, instruction_content) 
        }
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        chatgpt_settings = {'model': settings.model, 'openai_key': user.openai_key}
        chatgpt_json = await Chatgpt_json.create(chatgpt_settings)
        return cls(chatgpt_json, prompts, agent_uuid)
    
    @staticmethod
    async def get_settings_by_id(db: AsyncSession, id: int):
        return await get_settings_by_id(db, id)
    
    @staticmethod
    async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str):
        agent = await get_agent_by_uuid(db, agent_uuid)
        return agent if agent else ''

    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''    
    
    async def website_client(self, data):
        prompt = [{"role": "system", "content": self.prompts.get('system')}]
        prompt.append({"role": "user", "content": "{}".format(data.body)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return json.dumps(result)