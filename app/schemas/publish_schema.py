from pydantic import BaseModel

class PublishWechat(BaseModel):
    accessToken: str
    agentUuid: str