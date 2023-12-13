import json
from ..LLMs.chatgpt import Chatgpt_json, Chatgpt
from ..prompt_service import get_prompt_by_name
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..user_service import get_user_by_uuid
from ..settings_service import get_settings_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_spl_to_splform, convert_splform_to_spl
from ...schemas.agent_schema import AgentResponseWorkspace

class SPLFormCopilot:
    def __init__(self, chatgpt_json, chatgpt, prompts, agent_uuid) -> None:
        self.prompts = prompts
        self.chatgpt_json = chatgpt_json
        self.chatgpt = chatgpt
        self.agent_uuid = agent_uuid

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid: str):
        prompts = {
            'conv_per_aud_des': await cls.get_prompt(db, 'conv_per_aud_des'),
            'context_control': await cls.get_prompt(db, 'context_control'),
            'instruction_content': await cls.get_prompt(db, 'instruction_content'),
            'spl_guardrails': await cls.get_prompt(db, 'spl_guardrails'),
            'splform_copilot': await cls.get_prompt(db, 'splform_copilot'),
            'copilot_chat': await cls.get_prompt(db, 'copilot_chat'),
            'copilot_suggest': await cls.get_prompt(db, 'copilot_suggest')
        }
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        chatgpt_settings = {'model': settings.model, 'openai_key': user.openai_key}
        chatgpt_json = await Chatgpt_json.create(chatgpt_settings)
        chatgpt = await Chatgpt.create(chatgpt_settings)
        return cls(chatgpt_json, chatgpt, prompts, agent_uuid)

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
    
    async def copilot_chat(self, system_prompt, message, agent):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[user description]: {}\n[SPL]: {}".format(message, agent.spl)})
        response = await self.chatgpt.process_message(prompt)
        yield response.choices[0].message.content

    async def copilot_suggest(self, system_prompt, agent):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[SPL]: {}".format(agent.spl)})
        response = await self.chatgpt_json.process_message(prompt)
        yield response.choices[0].message.content
    
    async def copilot_spl(self, db: AsyncSession, message, agent):
        prompt = [{"role": "system", "content": self.prompts.get('splform_copilot')}]
        prompt.append({"role": "user", "content": "[user description]: {}\n[SPL]: {}".format(message, agent.spl)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        splform = convert_spl_to_splform(result)
        agent_data = {'spl': json.dumps(result), 'spl_form': json.dumps(splform)}
        agent = await SPLFormCopilot.update_agent(db, self.agent_uuid, agent_data)
        yield json.dumps(AgentResponseWorkspace.model_validate(agent, from_attributes=True).model_dump())

    async def initialize_spl(self, db: AsyncSession, message):
        personas, audiences, terminologies, instructions = await self.conv_per_aud_des(self.prompts.get('conv_per_aud_des'), message)
        splform = {'formData': []}
        personaData = {
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Persona",
            "sections": [
                {
                    "subSectionId": str(i),
                    "sequencialId":str(i),
                    "subSectionType": "Description",
                    "content": persona
                } for i, persona in enumerate(personas)
            ]
        }
        yield json.dumps(personaData)
        splform['formData'].append(personaData)
        audienceData = {
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Audience",
            "sections": [
                {
                    "subSectionId": str(i),
                    "sequencialId":str(i),
                    "subSectionType": "Description",
                    "content": audience
                } for i, audience in enumerate(audiences)
            ]
        }
        yield json.dumps(audienceData)
        splform['formData'].append(audienceData)
        terminologyData = {
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Terminology",
            "sections": [
                {
                    "subSectionId": str(i),
                    "sequencialId":str(i),
                    "subSectionType": "Term",
                    "content": terminology
                } for i, terminology in enumerate(terminologies)
            ]
        }
        yield json.dumps(terminologyData)
        splform['formData'].append(terminologyData)
        context_rules = await self.context_control(self.prompts.get('context_control'), message, personas, audiences, instructions)
        contextRuleData ={
            "sectionId": str(len(splform['formData'])),
            "sectionType": "ContextControl",
            "sections": [
                {
                    "subSectionId": str(i),
                    "sequencialId":str(i),
                    "subSectionType": "Rule",
                    "content": context_rule
                } for i, context_rule in enumerate(context_rules)
            ]
        }
        yield json.dumps(contextRuleData)
        splform['formData'].append(contextRuleData)
        guardrails = await self.guardrails(self.prompts.get('spl_guardrails'), message, personas, audiences, instructions)
        guardrailsData ={
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Guardrails",
            "sections": [
                {
                    "subSectionId": str(i),
                    "sequencialId":str(i),
                    "subSectionType": name,
                    "content": description
                } for i, (name, description) in enumerate(guardrails.items())
            ]
        }
        yield json.dumps(guardrailsData)
        splform['formData'].append(guardrailsData)
        for instruction_name in instructions.keys():
            instruction = instructions[instruction_name]
            instruction_command, instruction_rule = await self.instruction_content(self.prompts.get('instruction_content'), message, personas, audiences, instruction)
            instructionData = {
                "sectionId": str(len(splform['formData'])),
                "sectionType": 'Instruction',
                "sections": []
            }

            try:
                instructionData['sections'].append({
                    "subSectionId": str(len(instructionData['sections'])),
                    "sequencialId":str(0),
                    "subSectionType": "Name",
                    "content": instruction_name
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                for i, command in enumerate(instruction_command):
                    instructionData['sections'].append(
                        {
                            "subSectionId": str(len(instructionData['sections'])),
                            "sequencialId":str(i),
                            "subSectionType": "Command",
                            "content": command
                        } 
                ) 
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                for i, rule in enumerate(instruction_rule):
                    instructionData['sections'].append(
                        {
                            "subSectionId": str(len(instructionData['sections'])),
                            "sequencialId":str(i),
                            "subSectionType": "Rule",
                            "content": rule
                        } 
                )
            except Exception as e:
                print(f"Error while adding section: {e}")
            yield json.dumps(instructionData)
            splform['formData'].append(instructionData)
        spl = convert_splform_to_spl(splform)
        agent_data = {'spl': json.dumps(spl), 'spl_form': json.dumps(splform)}
        agent = await SPLFormCopilot.update_agent(db, self.agent_uuid, agent_data)
        yield json.dumps(AgentResponseWorkspace.model_validate(agent, from_attributes=True).model_dump())

    async def conv_per_aud_des(self, system_prompt, user_description):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}".format(user_description)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['result']["Character"], result['result']["Audience"], result['result']["Terminology"], result['result']["Instructions"]

    async def context_control(self, system_prompt, user_description, persona, audience, instructions):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}\n[Character]: {}\n[Audience]: {}\n[Character Instruction]: {}".format(user_description, persona, audience, instructions)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['result']['Restraints']
    
    async def guardrails(self, system_prompt, user_description, persona, audience, instructions):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}\n[Character]: {}\n[Audience]: {}\n[Character Instruction]: {}".format(user_description, persona, audience, instructions)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['guardrails']

    async def instruction_content(self, system_prompt, user_description, persona, audience, instructions):
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}\n[Character]: {}\n[Audience]: {}\n[Character Instruction]: {}".format(user_description, persona, audience, instructions)})
        response = await self.chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['result']["Commands"], result['result']["Restraints"]
    

    async def splform_copilot(self, db, message):
        agent = await SPLFormCopilot.get_agent_by_uuid(db, self.agent_uuid)
        if agent.spl:
            async for response in self.copilot_chat(self.prompts.get('copilot_chat'), message, agent):
                yield response
            async for response in self.copilot_spl(db, message, agent):
                yield response
        else:
            yield json.dumps({'copilot': 'Initializing agent...Creating SPL form...'})
            async for response in  self.initialize_spl(db, message):
                yield response
        async for response in self.copilot_suggest(self.prompts.get('copilot_suggest'), await SPLFormCopilot.get_agent_by_uuid(db, self.agent_uuid)):
            yield response
        yield "__END_OF_RESPONSE__"
        