import json
from ..LLMs.chatgpt import Chatgpt_json
from ..LLMs.assistant import Assistant
from ..agent_service import get_agent_by_uuid, edit_agent_by_uuid
from ..prompt_service import get_prompt_by_name
from ..settings_service import get_settings_by_id, edit_settings
from ..user_service import get_user_by_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.settings_schema import SettingsResponse
import asyncio
import copy

class RunChain:
    def __init__(self, client, assistant, thread, chain, chatgpt_json, prompts) -> None:
        self.client = client
        self.assistant = assistant
        self.thread = thread
        self.chain = chain
        self.chatgpt_json = chatgpt_json
        self.prompts = prompts

    @classmethod
    async def create(cls, db: AsyncSession, agent_uuid):
        prompts = {
            'chain_instruction': await cls.get_prompt(db, 'chain_instruction'),
            'if_condition': await cls.get_prompt(db, 'if_condition'),
        }
        agent = await cls.get_agent_by_uuid(db, agent_uuid)
        settings = await cls.get_settings_by_id(db, agent.settings_id)
        user = await cls.get_user_by_uuid(db, agent.owner_uuid)
        chatgpt_settings = {'model': settings.model, 'openai_key': user.openai_key}
        chatgpt_json = await Chatgpt_json.create(chatgpt_settings)
        settings = SettingsResponse.model_validate(settings, from_attributes=True).model_dump()
        assistant_init = await Assistant.create({'openai_key': user.openai_key})
        chain = json.loads(agent.chain)
        settings.update({'instruction': "{}\n[Persona]: {}\n[Audience]: {}\n[Terminology]: {}".format(prompts.get('chain_instruction'), chain.get('Persona', ''), chain.get('Audience', ''), chain.get('Terminology', ''))})
        assistant = await assistant_init.load_assistant(settings)
        assistant = await assistant_init.update_assistant(settings)
        await cls.update_settings(db, agent.settings_id, settings)
        thread = await assistant_init.create_thread()
        return cls(assistant_init.client, assistant, thread, chain, chatgpt_json, prompts)
    
    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await get_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent_by_uuid(db, agent_id, update_data)
    
    @staticmethod
    async def get_settings_by_id(db: AsyncSession, id: int):
        return await get_settings_by_id(db, id)
    
    @staticmethod
    async def update_settings(db: AsyncSession, settings_id: int, update_data: dict):
        return await edit_settings(db, settings_id, update_data)
    
    @staticmethod
    async def get_agent_by_uuid(db: AsyncSession, agent_uuid: str):
        agent = await get_agent_by_uuid(db, agent_uuid)
        return agent if agent else ''

    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''  
    
    async def run_step(self, message, file_ids):
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message,
            file_ids=file_ids)

        run = await self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id)

        while run.status == "queued":
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id)

        while run.status == "in_progress":
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id)

        messages = await self.client.beta.threads.messages.list(thread_id=self.thread.id)
        return messages.data[0].content[0].text.value


    async def run_chain(self, message_data, step_mode):
        if step_mode:
            async for response in self.run_chain_step(message_data):
                yield response
        else:
            async for response in self.run_chain_continue(message_data):
                yield response

    async def run_chain_step(self, message_data):
        steps = self.chain.get('Steps')
        step_id = json.loads(message_data).get('step_id')
        message = json.loads(message_data).get('message')
        file_ids = json.loads(message_data).get('file_ids', [])
        step = steps[step_id]
        output_message = copy.deepcopy(step)    
        if len(step.get('next_steps')) == 0:
            message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[[Input_message]]: {}".format(step.get('step_type'), step.get('step_instruction'), message), file_ids)
            output_message.update({"console": message})         
            output_message.update({"result": message})
            output_message.update({"next_step": ''})
            yield json.dumps(output_message)
            # yield "__END_OF_RESPONSE__"
        elif len(step.get('next_steps')) > 1:
            message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), file_ids)
            output_message.update({"console": message})
            next_steps = [next_step for next_step in steps if next_step.get('step_id') in step.get('next_steps')]
            prompt = [{"role": "system", "content": self.prompts.get('if_condition')}]
            prompt.append({"role": "user", "content": "[current step]: {}, [step output]: {}, [next steps]: {}".format(step, message, next_steps)})
            # yield json.dumps({"console": "Identify next step"})
            response = await self.chatgpt_json.process_message(prompt)
            result = json.loads(response.choices[0].message.content)
            step_id = result.get('step_id')
            output_message.update({"next_step": str(step_id)})
            yield json.dumps(output_message)
        else:
            message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), file_ids)
            output_message.update({"console": message})
            step_id = step.get('next_steps')[0]
            output_message.update({"next_step": str(step_id)})
            yield json.dumps(output_message)

    
    async def run_chain_continue(self, message_data):
        steps = self.chain.get('Steps')
        step_id = 0
        message = json.loads(message_data).get('message')
        file_ids = json.loads(message_data).get('file_ids', [])
        if len(file_ids):
            step = steps[step_id]
            output_message = copy.deepcopy(step)
            json.dumps({"console": "Loading files..."})
            message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), file_ids)
            output_message.update({"console": message})           
            step_id = step.get('next_steps')[0]
            output_message.update({"next_step": str(step_id)})  
            yield json.dumps(output_message)       
        while True:
            step = steps[step_id]
            output_message = copy.deepcopy(step)
            if len(step.get('next_steps')) == 0:
                message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), [])   
                output_message.update({"console": message})         
                output_message.update({"result": message})
                output_message.update({"next_step": ''})
                yield json.dumps(output_message)
                yield "__END_OF_RESPONSE__"
                break
            elif len(step.get('next_steps')) > 1:
                message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), [])
                output_message.update({"console": message})
                next_steps = [next_step for next_step in steps if next_step.get('step_id') in step.get('next_steps')]
                prompt = [{"role": "system", "content": self.prompts.get('if_condition')}]
                prompt.append({"role": "user", "content": "[current step]: {}, [step output]: {}, [next steps]: {}".format(step, message, next_steps)})
                json.dumps({"console": "Identify next step"})
                response = await self.chatgpt_json.process_message(prompt)
                result = json.loads(response.choices[0].message.content)
                step_id = result.get('step_id')
                output_message.update({"next_step": str(step_id)})
                yield json.dumps(output_message)
            else:
                message = await self.run_step("[step_type]:{}\n[step_instruction]:{}\n[Input_message]: {}".format(step.get('step_type'), step.get('step_instruction'), message), [])               
                output_message.update({"console": message})
                step_id = step.get('next_steps')[0]
                output_message.update({"next_step": str(step_id)})
                yield json.dumps(output_message)
