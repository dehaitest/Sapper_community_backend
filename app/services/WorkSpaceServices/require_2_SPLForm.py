import json
from ..LLMs.chatgpt import Chatgpt_json
from ..prompt_service import select_prompt_by_name
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.data_manager import spl_data_manager

class Require2SPLForm:
    def __init__(self, user_description, prompt1, prompt2, prompt3) -> None:
        self.user_description = user_description
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.prompt3 = prompt3

    @classmethod
    async def create(cls, db: AsyncSession, user_description):
        prompt1 = await cls.get_prompt(db, 'conv_per_aud_des')
        prompt2 = await cls.get_prompt(db, 'context_control')
        prompt3 = await cls.get_prompt(db, 'instruction_content')
        return cls(user_description, prompt1, prompt2, prompt3)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await select_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''

    async def conv_per_aud_des(self, system_prompt, user_description):
        chatgpt_json = Chatgpt_json()
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}".format(user_description)})
        response = await chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['result']["Character"], result['result']["Audience"], result['result']["Instructions"]

    async def context_control(self, system_prompt, user_description, persona, audience, instructions):
        chatgpt_json = Chatgpt_json()
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}\n[Character]: {}\n[Audience]: {}\n[Character Instruction]: {}".format(user_description, persona, audience, instructions)})
        response = await chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        return result['result']['Restraints']

    async def instruction_content(self, system_prompt, user_description, persona, audience, instructions):
        chatgpt_json = Chatgpt_json()
        prompt = [{"role": "system", "content": system_prompt}]
        prompt.append({"role": "user", "content": "[User task description]: {}\n[Character]: {}\n[Audience]: {}\n[Character Instruction]: {}".format(user_description, persona, audience, instructions)})
        response = await chatgpt_json.process_message(prompt)
        result = json.loads(response.choices[0].message.content)
        print(result)
        return result['result']["Commands"], result['result']["Restraints"]

    async def require_2_splForm(self):
        persona, audience, instructions = await self.conv_per_aud_des(self.prompt1, self.user_description)
        personaData = {
            "sectionId": '1',
            "sectionType": "Persona",
            "section": [
                {
                    "sectionId": "S1",
                    "subSectionType": "Description",
                    "content": persona
                }
            ]
        }
        yield json.dumps(personaData)
        audienceData = {
            "sectionId": '2',
            "sectionType": "Audience",
            "section": [
                {
                    "subSectionId": "S1",
                    "subSectionType": "Description",
                    "content": audience
                }
            ]
        }
        yield json.dumps(audienceData)
        context_rule = await self.context_control(self.prompt2, self.user_description, persona, audience, instructions)
        contextRuleData ={
            "sectionId": '3',
            "sectionType": "ContextControl",
            "section": [
                {
                    "subSectionId": "S1",
                    "subSectionType": "Rules",
                    "content": context_rule
                }
            ]
        }
        yield json.dumps(contextRuleData)
        for i, instruction_name in enumerate(instructions.keys()):
            instruction = instructions[instruction_name]
            instruction_command, instruction_rule = await self.instruction_content(self.prompt3, self.user_description, persona, audience, instruction)
            print(instruction_rule, "\n", instruction_command)
            instructionData = {
                "sectionId": str(i + 4),
                "sectionType": 'Instruction',
                "section": []
            }

            try:
                instructionData['section'].append({
                    "subSectionId": "S5",
                    "subSectionType": "Name",
                    "content": instruction_name
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                instructionData['section'].append({
                    "subSectionId": "S1",
                    "subSectionType": "Commands",
                    "content": instruction_command
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            try:
                instructionData['section'].append({
                    "subSectionId": "S4",
                    "subSectionType": "Rules",
                    "content": instruction_rule
                })
            except Exception as e:
                print(f"Error while adding section: {e}")

            yield json.dumps(instructionData)
        yield "__END_OF_RESPONSE__"
