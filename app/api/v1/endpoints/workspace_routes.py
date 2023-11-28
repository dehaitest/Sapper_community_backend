import json
from fastapi import APIRouter, WebSocket, Depends
from ....services.WorkSpaceServices.require_2_SPLForm import Require2SPLForm
from ....services.get_LLM_response import GetLLMResponse
from ....services.LLMs.chatgpt import Chatgpt
from ....core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session

router = APIRouter()

@router.websocket("/ws/sapperchain/require2SPLForm")
async def require_2_SPLForm(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        require2SPLForm_instance = await Require2SPLForm.create(db, data)
        async for response in require2SPLForm_instance.require_2_splForm():
            print('websocket:', response)
            await websocket.send_text(response)

@router.websocket("/ws/sapperchain/NLText2SPLForm")
async def NLText_2_SPLForm(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        chat_service = Chatgpt(settings.OPENAI_KEY)
        # require2SPLForm_instance = Require2SPLForm(data, chat_service.process_message)
        # async for part in require2SPLForm_instance.require_2_splForm():
        #     await websocket.send_text(part)

@router.websocket("/ws/sapperchain/SPLForm2NLText")
async def SPLForm_2_NLText(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        chat_service = Chatgpt(settings.OPENAI_KEY)
        # require2SPLForm_instance = Require2SPLForm(data, chat_service.process_message)
        # async for part in require2SPLForm_instance.require_2_splForm():
        #     await websocket.send_text(part)

@router.websocket("/ws/sapperchain/formCopilot")
async def form_copilot(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        chat_service = Chatgpt(settings.OPENAI_KEY)
        # require2SPLForm_instance = Require2SPLForm(data, chat_service.process_message)
        # async for part in require2SPLForm_instance.require_2_splForm():
        #     await websocket.send_text(part)

@router.websocket("/ws/sapperchain/GetLLMResponse")
async def get_LLM_response(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        chat_service = Chatgpt(settings.OPENAI_KEY)
        getLLMResponse_instance = GetLLMResponse(chat_service.process_message)
        async for part in getLLMResponse_instance.get_LLM_Response(json.loads(data)):
            await websocket.send_text(part)
