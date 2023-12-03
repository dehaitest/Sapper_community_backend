import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from ..agent_service import create_agent
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_conversion import convert_splform_to_spl

class RequireToSPLForm:
    def __init__(self, chatgpt_json, prompt_conv_per_aud_des, prompt_context_control, prompt_instruction_content, prompt_spl_guardrails) -> None:
        self.prompt_conv_per_aud_des = prompt_conv_per_aud_des
        self.prompt_context_control = prompt_context_control
        self.prompt_instruction_content = prompt_instruction_content
        self.prompt_spl_guardrails = prompt_spl_guardrails
        self.chatgpt_json = chatgpt_json


    @classmethod
    async def create(cls, db: AsyncSession):
        prompt_conv_per_aud_des = await cls.get_prompt(db, 'conv_per_aud_des')
        prompt_context_control = await cls.get_prompt(db, 'context_control')
        prompt_instruction_content = await cls.get_prompt(db, 'instruction_content')
        prompt_spl_guardrails = await cls.get_prompt(db, 'spl_guardrails')
        chatgpt_json = await Chatgpt_json.create()
        return cls(chatgpt_json, prompt_conv_per_aud_des, prompt_context_control, prompt_instruction_content, prompt_spl_guardrails)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await select_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def create_new_agent(db: AsyncSession, agent_data: dict):
        return await create_agent(db, agent_data)
        
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

    async def require_to_splForm(self, db: AsyncSession, user_description):
        personas, audiences, terminologies, instructions = await self.conv_per_aud_des(self.prompt_conv_per_aud_des, user_description)
        splform = {'formData': []}
        personaData = {
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Persona",
            "sections": [
                {
                    "subSectionId": str(i),
                    "subSectionType": "Description-{}".format(i),
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
                    "subSectionType": "Description-{}".format(i),
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
                    "subSectionType": "Description-{}".format(i),
                    "content": terminology
                } for i, terminology in enumerate(terminologies)
            ]
        }
        yield json.dumps(terminologyData)
        splform['formData'].append(terminologyData)
        context_rules = await self.context_control(self.prompt_context_control, user_description, personas, audiences, instructions)
        contextRuleData ={
            "sectionId": str(len(splform['formData'])),
            "sectionType": "ContextControl",
            "sections": [
                {
                    "subSectionId": str(i),
                    "subSectionType": "Rule-{}".format(i),
                    "content": context_rule
                } for i, context_rule in enumerate(context_rules)
            ]
        }
        yield json.dumps(contextRuleData)
        splform['formData'].append(contextRuleData)
        guardrails = await self.guardrails(self.prompt_spl_guardrails, user_description, personas, audiences, instructions)
        guardrailsData ={
            "sectionId": str(len(splform['formData'])),
            "sectionType": "Guardrails",
            "sections": [
                {
                    "subSectionId": str(i),
                    "subSectionType": name,
                    "content": description
                } for i, (name, description) in enumerate(guardrails.items())
            ]
        }
        yield json.dumps(guardrailsData)
        splform['formData'].append(guardrailsData)
        for i, instruction_name in enumerate(instructions.keys()):
            instruction = instructions[instruction_name]
            instruction_command, instruction_rule = await self.instruction_content(self.prompt_instruction_content, user_description, personas, audiences, instruction)
            instructionData = {
                "sectionId": str(len(splform['formData'])),
                "sectionType": 'Instruction' + '-' + str(i),
                "sections": []
            }

            try:
                instructionData['sections'].append({
                    "subSectionId": str(len(instructionData['sections'])),
                    "subSectionType": "Name",
                    "content": instruction_name
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                instructionData['sections'].append({
                    "subSectionId": str(len(instructionData['sections'])),
                    "subSectionType": "Commands",
                    "content": instruction_command
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                instructionData['sections'].append({
                    "subSectionId": str(len(instructionData['sections'])),
                    "subSectionType": "Rules",
                    "content": instruction_rule
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            yield json.dumps(instructionData)
            splform['formData'].append(instructionData)
        spl = convert_splform_to_spl(splform)
        agent_data = {'spl': json.dumps(spl), 'spl_form': json.dumps(splform)}
        new_agent = await RequireToSPLForm.create_new_agent(db, agent_data)
        yield json.dumps(new_agent.to_dict())
        yield "__END_OF_RESPONSE__"
