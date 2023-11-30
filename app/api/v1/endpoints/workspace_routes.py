import json
from fastapi import APIRouter, WebSocket, Depends
from ....services.WorkSpaceServices.require_to_splform import RequireToSPLForm
from ....services.WorkSpaceServices.splform_to_nl import SPLForm_to_NL
from ....services.WorkSpaceServices.nl_to_splform import NL_to_SPLForm
from ....services.get_LLM_response import GetLLMResponse
from ....services.LLMs.chatgpt import Chatgpt
from ....core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session

router = APIRouter()

@router.websocket("/ws/sapperchain/requiretosplform")
async def require_to_splform_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        requireToSPLForm_instance = await RequireToSPLForm.create(db, data)
        async for response in requireToSPLForm_instance.require_to_splForm(db):
            await websocket.send_text(response)

@router.websocket("/ws/sapperchain/nltosplform")
async def NLText_to_SPLForm_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    NL_to_SPLForm_instance = await NL_to_SPLForm.create(db)
    async for response in NL_to_SPLForm_instance.nl_to_splform(db, data):
        await websocket.send_text(response)

@router.websocket("/ws/sapperchain/splformtonl")
async def splform_to_nl_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    SPLForm_to_NL_instance = await SPLForm_to_NL.create(db)
    async for response in SPLForm_to_NL_instance.splform_to_nl(db, data):
        await websocket.send_text(response)

@router.websocket("/ws/sapperchain/formcopilot")
async def form_copilot_endpoint(websocket: WebSocket):
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
