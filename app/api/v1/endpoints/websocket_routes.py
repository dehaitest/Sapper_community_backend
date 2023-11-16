from fastapi import APIRouter, WebSocket
from ....services.chat_service import ChatService

router = APIRouter()

@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    chat_service = ChatService()
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for part in chat_service.process_message(data):
            await websocket.send_text(part)
