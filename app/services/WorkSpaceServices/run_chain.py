import json
from ..LLMs.chatgpt import Chatgpt_json
from ..LLMs.assistant import Assistant
from ..agent_service import select_agent_by_id, edit_agent
from ..prompt_service import select_prompt_by_name
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class RunChain:
    def __init__(self, client, assistant, thread, chain, chatgpt_json, prompt_if_condition) -> None:
        self.client = client
        self.assistant = assistant
        self.thread = thread
        self.chain = chain
        self.chatgpt_json = chatgpt_json
        self.prompt_if_condition = prompt_if_condition

    @classmethod
    async def create(cls, db: AsyncSession, message_data):
        agent = await cls.get_agent_by_id(db, json.loads(message_data)['id'])
        agent_settings = json.loads(agent.settings)
        chain = json.loads(agent.chain)
        instruction = await cls.get_prompt(db, 'instruction')
        agent_settings.update({'instruction': "{}, {}, {}, {}".format(instruction, chain.get('Persona', ''), chain.get('Audience', ''), chain.get('Terminology', ''))})
        assistant_init = await Assistant.create()
        if 'assistant_id' in agent_settings and agent_settings.get('assistant_id'):
            assistant = await assistant_init.load_assistant(agent_settings)
            assistant = await assistant_init.update_assistant(agent_settings)
        else:
            assistant = await assistant_init.create_assistant(agent_settings)
            agent_settings.update({'assistant_id': assistant.id})
        await cls.update_agent(db, agent.id, {'settings': json.dumps(agent_settings)}) 
        thread = await assistant_init.create_thread()
        chatgpt_json = await Chatgpt_json.create()
        prompt_if_condition = await cls.get_prompt(db, 'if_condition')
        return cls(assistant_init.client, assistant, thread, chain, chatgpt_json, prompt_if_condition)
    
    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await select_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''
    
    @staticmethod
    async def update_agent(db: AsyncSession, agent_id: int, update_data: dict):
        return await edit_agent(db, agent_id, update_data)
    
    @staticmethod
    async def get_agent_by_id(db: AsyncSession, agent_id: int):
        agent = await select_agent_by_id(db, agent_id)
        return agent if agent else ''
    
    async def run_step(self, message):
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message)

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

    
    async def run_chain(self, message_data):
        steps = self.chain.get('Steps')
        step_id = 0
        message = message_data
        while True:
            step = steps[step_id]
            if len(step.get('next_steps')) == 0:
                yield json.dumps(step)
                message = await self.run_step("{} Input message: {}".format(step.get('step_instruction'), message))               
                yield message
                yield "__END_OF_RESPONSE__"
                break
            elif len(step.get('next_steps')) > 1:
                yield json.dumps(step)
                message = await self.run_step("{} Input message: {}".format(step.get('step_instruction'), message))
                yield message
                next_steps = [next_step for next_step in steps if next_step.get('step_id') in step.get('next_steps')]
                prompt = [{"role": "system", "content": self.prompt_if_condition}]
                prompt.append({"role": "user", "content": "[current step]: {}, [step output]: {}, [next steps]: {}".format(step, message, next_steps)})
                yield 'Identify next step'
                response = await self.chatgpt_json.process_message(prompt)
                result = json.loads(response.choices[0].message.content)
                step_id = result.get('step_id')
                yield 'next step {}'.format(step_id)
            else:
                yield json.dumps(step)
                message = await self.run_step("{} Input message: {}".format(step.get('step_instruction'), message))               
                yield message
                step_id = step.get('next_steps')[0]
                yield 'next step {}'.format(step_id)
