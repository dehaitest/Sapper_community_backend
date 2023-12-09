import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..user_service import get_user_by_uuid
from ..settings_service import get_settings_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.agent_schema import AgentResponseWorkspace

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
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        chatgpt_settings = {'model': settings.model, 'openai_key': user.openai_key}
        chatgpt_json = await Chatgpt_json.create(chatgpt_settings)
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
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''

    @staticmethod
    async def update_agent(db: AsyncSession, agent_uuid: str, update_data: dict):
        return await edit_agent_by_uuid(db, agent_uuid, update_data)
    
    async def spl_to_cfp(self, spl):
        prompt = [{"role": "system", "content": self.prompts.get('generate_cfp')}]
        prompt.append({"role": "user", "content": "[SPL]: {}".format(spl)})
        response = await self.chatgpt_json.process_message(prompt)
        return json.loads(response.choices[0].message.content)
    
    async def cfp_debugging(self, persona, cfp):
        prompt = [{"role": "system", "content": self.prompts.get('cfp_debug')}]
        prompt.append({"role": "user", "content": "[SPL]: {}, [ExecutionPaths]: {}".format(persona, cfp)})
        response = await self.chatgpt_json.process_message(prompt)
        return json.loads(response.choices[0].message.content)
    
    async def splform_to_cfp(self, db):
        agent = await SPLFormToCFP.get_agent_by_uuid(db, self.agent_uuid)
        spl = json.loads(agent.spl)
        instructions = {}
        for key, value in spl.items():
            if 'Instruction' in key:
                instructions[key] = instructions.get(key, value)
        cfp = await self.spl_to_cfp(instructions)
        result = await self.cfp_debugging(spl["Persona"], cfp)
        agent_data = {'cfp': json.dumps(result)}
        agent = await SPLFormToCFP.update_agent(db, self.agent_uuid, agent_data)
        yield json.dumps(AgentResponseWorkspace.model_validate(agent, from_attributes=True).model_dump())
        yield "__END_OF_RESPONSE__"