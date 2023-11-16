from fastapi import APIRouter, WebSocket
from ...services.chat_service import ChatService

router = APIRouter()

@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, chat_service: ChatService = ChatService()):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = await chat_service.process_message(data)
        await websocket.send_text(response)
