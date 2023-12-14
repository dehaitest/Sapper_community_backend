import openai

class Assistant:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls, settings: dict):
        instance = cls()
        await instance.async_init(settings)
        return instance

    async def async_init(self, settings: dict):
        self.client = openai.AsyncOpenAI(api_key=settings.get('openai_key'))

    async def create_assistant(self, agent_settings: dict):
        try:
            assistant = await self.client.beta.assistants.create(
                instructions=agent_settings.get('instruction', ''),
                model=agent_settings.get('model'),
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when creating assistant: {e}")

    async def load_assistant(self, agent_settings: dict):
        try:
            assistant = await self.client.beta.assistants.retrieve(
                assistant_id=agent_settings.get('assistant_id')
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when loading assistant: {e}")

    async def update_assistant(self, agent_settings: dict):
        try:
            assistant = await self.client.beta.assistants.create(
                instructions=agent_settings.get('instruction', ''),
                model=agent_settings.get('model'),
                tools= [tool.get('detail') for tool in agent_settings.get('tools') if tool.get('active')] if 'tools' in agent_settings and agent_settings['tools'] else [],
                file_ids=[file.get('file_id') for file in agent_settings.get('files') if file.get('active')] if 'files' in agent_settings and agent_settings['files'] else [],
            )
            return assistant
        except Exception as e:
            print(f"An error occurred when updating assistant: {e}")

    async def create_thread(self):
        try:
            return await self.client.beta.threads.create()
        except Exception as e:
            print(f"An error occurred when creating thread: {e}")
