from ..LLMs.assistant import Assistant
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from ..user_service import get_user_by_uuid

class UploadUserFile:
    def __init__(self, client) -> None:
        self.client = client

    @classmethod
    async def create(cls, db, user_uuid):
        user = await cls.get_user_by_uuid(db, user_uuid)
        assistant_init = await Assistant.create({'openai_key': user.openai_key})
        return cls(assistant_init.client)
    
    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
        user = await get_user_by_uuid(db, user_uuid)
        return user if user else ''  
    
    async def upload_user_file(self, user_file):
        try:
            buffer = BytesIO()
            content = await user_file.read()
            buffer.write(content)
            buffer.seek(0)
            file = await self.client.files.create(
                file=buffer,
                purpose='assistants'
            )
            return {'file_name': user_file.filename, 'file_id': file.id, 'content_type': user_file.content_type, 'active': 0}
        except Exception as e:
            print(f"An error occurred when uploading file: {e}")
        finally:
            buffer.close()
