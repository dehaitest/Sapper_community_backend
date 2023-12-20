from sqlalchemy.ext.asyncio import AsyncSession
from ..prompt_service import get_prompt_by_name


class WechatTemplate:
    def __init__(self, template) -> None:
        self.template = template

    @classmethod
    async def create(cls, db: AsyncSession):
        template =  await cls.get_prompt(db, 'wechat_template')
        return cls(template)

    @staticmethod
    async def get_prompt(db: AsyncSession, name: str):
        prompt = await get_prompt_by_name(db, name)
        return prompt.prompt if prompt else ''

    async def generate_client(self, data):
        url = f"ws://localhost:8000/ws/client/wechat?token={data.accessToken}&agent_uuid={data.agentUuid}"
        return self.template.replace("{{url}}", url)