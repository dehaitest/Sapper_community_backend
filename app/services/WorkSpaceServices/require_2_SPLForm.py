import json
import re
from app.services.LLMs.Chatgpt import Chatgpt
import asyncio
import os


class Require2SPLForm:
    def __init__(self, user_description, process) -> None:
        self.user_description = user_description
        self.process = process
        self.base_path = os.path.dirname(__file__)  # 获取当前文件的目录
        self.path = os.path.join(self.base_path, '..', 'Prompts', 'require2form')
        self.prompt1 = os.path.join(self.path, 'system1')
        self.prompt2 = os.path.join(self.path, 'system2')
        self.prompt3 = os.path.join(self.path, 'system3')

    def read_txt_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

    async def conv_per_aud_des(self, prompt_path, user_description):
        system = self.read_txt_file(prompt_path)
        prompt = [{"role": "system", "content": f"{system}"}]
        information = f'[User task description]: {user_description}'
        prompt.append({"role": "user", "content": information})
        per_aud_des_content = ""
        print(prompt)
        async for part in self.process(prompt):
            if part == "__END_OF_RESPONSE__":
                break
            per_aud_des_content += part

        print(per_aud_des_content)
        # Regular expressions to match the patterns
        character_pattern = r"\[Character]:\s+(.+)"
        audience_pattern = r"\[Audience]:\s+(.+)"
        instruction_pattern = r"\[Character Instruction]:([\s\S]*)"

        # Finding matches
        character_match = re.search(character_pattern, per_aud_des_content)
        audience_match = re.search(audience_pattern, per_aud_des_content)
        instruction_match = re.search(instruction_pattern, per_aud_des_content)

        # Extracting text from matches
        character = character_match.group(1) if character_match else ''
        audience = audience_match.group(1) if audience_match else ''
        instruction = instruction_match.group(1).strip() if instruction_match else '{}'

        # Replacing characters and splitting the instruction part
        instruction = json.loads(instruction)

        # Printing the results
        print("Character:", character)
        print("Audience:", audience)
        print("Instruction Names:", instruction)

        return [character, audience, instruction]

    async def context_control(self, prompt_path, user_description, persona, audience, instructions):
        system = self.read_txt_file(prompt_path)
        prompt = [{"role": "system", "content": system}]
        information = f"[User task description]: {user_description}\n[Character]: {persona}\n[Audience]: {audience}\n[Character Instruction]: {json.dumps(instructions)}"
        prompt.append({"role": "user", "content": information})
        control_content = ""
        async for part in self.process(prompt):
            if part == "__END_OF_RESPONSE__":
                break
            control_content += part
        control_content = control_content.replace("：", ":")
        restraint_text = control_content.replace("[Context Restraint]:", "").strip()
        print(restraint_text)
        restraint_array = json.loads(restraint_text)

        return restraint_array

    async def instruction_content(self, prompt_path, user_description, persona, audience, instructions):
        system = self.read_txt_file(prompt_path)
        prompt = [{"role": "system", "content": system}]
        information = f"[User task description]: {user_description}\n[Character]: {persona}\n[Audience]: {audience}\n[Character Instruction]: {instructions}"
        prompt.append({"role": "user", "content": information})

        control_content = ""
        async for part in self.process(prompt):
            if part == "__END_OF_RESPONSE__":
                break
            control_content += part
        print(control_content)
        control_content = control_content.replace("：", ":")

        # 正则表达式
        command_pattern = r"\[Character Instruction Command\]: Array(\[.*?\])"
        restraint_pattern = r"\[Character Instruction Restraint\]: Array(\[.*?\])"

        # 使用re.DOTALL标志来匹配包括换行符在内的任何字符
        command_matches = re.search(command_pattern, control_content, re.DOTALL)
        restraint_matches = re.search(restraint_pattern, control_content, re.DOTALL)

        # 提取结果
        command_text = command_matches.group(1) if command_matches else "[]"
        restraint_text = restraint_matches.group(1) if restraint_matches else "[]"

        # Splitting the extracted content into arrays
        command_array = json.loads(command_text)
        restraint_array = json.loads(restraint_text)

        return command_array, restraint_array

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
        print(context_rule)
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


# api_key = config("OPENAI_KEY")
# if not api_key:
#     raise ValueError("OPENAI_KEY")
#
# # 使用示例
# chat_service = Chatgpt(api_key)
# require2SPLForm_instance = Require2SPLForm("generate math question", chat_service.process_message)
#
# async def main():
#     async for response_part in require2SPLForm_instance.require_2_splForm():
#         print(response_part)
#
# # 运行主程序
# if __name__ == "__main__":
#     asyncio.run(main())
