from sqlalchemy.ext.asyncio import AsyncSession
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid
from ..settings_service import get_settings_by_id
from ..user_service import get_user_by_uuid
from ..LLMs.chatgpt import Chatgpt_json
import json


class WebsiteTemplate:
    def __init__(self, chatgpt_json, prompts, agent_uuid) -> None:
        self.prompts = prompts
        self.chatgpt_json = chatgpt_json
        self.agent_uuid = agent_uuid

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid):
        prompts = {
            'visual_design': await cls.get_prompt(db, 'visual_design'),
            'design_page': await cls.get_prompt(db, 'design_page'),
            'code_generation': await cls.get_prompt(db, 'code_generation')
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

    async def code_generation(self, visual_design_template, design_page_template, commands):
        prompt = [{"role": "system", "content": self.prompts.get('code_generation')}]
        prompt.append({"role": "user", "content": "{Design_page_template Replacement Flag}: " + design_page_template + "\n{Visual_design_template Replacement Flag}: " + visual_design_template + "\n{task Replacement Flag}: " + commands})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result

    async def visual_design_template_generation(self, design_page_template):
        prompt = [{"role": "system", "content": self.prompts.get('visual_design')}]
        prompt.append({"role": "user", "content": "{Replacement Flag}: " + design_page_template})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return json.dumps(result)
    
    async def design_page_template_generation(self, commands):
        prompt = [{"role": "system", "content": self.prompts.get('design_page')}]
        prompt.append({"role": "user", "content": "{Replacement Flag}: " + commands})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return json.dumps(result)

    async def generate_client(self, db):
        agent = await WebsiteTemplate.get_agent_by_uuid(db, self.agent_uuid)
        spl = json.loads(agent.spl)
        result = {"ui":[]}
        for section_type, sections in spl.items():
            if 'Instruction' in section_type and sections.get('UI-0') == "True":
                commands = ','.join([value for key, value in sections.items() if "Command" in key])
                design_page_template = await self.design_page_template_generation(commands)
                visual_design_template = await self.visual_design_template_generation(design_page_template)
                code = await self.code_generation(visual_design_template, design_page_template, commands)
                code.update({"section": section_type})
                code.update({"name": sections.get('Name-0')})
                result["ui"].append(code)
        return json.dumps(result)