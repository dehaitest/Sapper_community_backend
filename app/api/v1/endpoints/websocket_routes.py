from fastapi import APIRouter, WebSocket
from ....services.chat_service import ChatService
from ....core.config import settings

router = APIRouter()

@router.websocket(settings.WEBSOCKET_ROUTE)
async def chat_websocket(websocket: WebSocket):
    chat_service = ChatService()
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for part in chat_service.process_message(data):
            print(part)
            await websocket.send_text(part)
