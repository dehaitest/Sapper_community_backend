from fastapi import APIRouter, WebSocket
from ....services.chat_service import ChatService
from ....services.database import SessionLocal
from ....services.user_service import validate_token 
from ....services.ClientServices.wechat import WechatClient

router = APIRouter()

@router.websocket('/ws/chat')
async def chat_websocket(websocket: WebSocket):
    chat_service = ChatService()
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for part in chat_service.process_message(data):
            await websocket.send_text(part)

# Wechat client
@router.websocket("/ws/client/wechat")
async def wechat_client_endpoint(websocket: WebSocket):
    async with SessionLocal() as db:
        await validate_token(db, websocket.query_params.get('token')) 
        WechatClient_instance = await WechatClient.create(db, websocket.query_params.get('agent_uuid'))
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for response in WechatClient_instance.wechat_client(data):
            await websocket.send_text(response)

# Robot client
@router.websocket("/ws/client/robot")
async def robot_client_endpoint(websocket: WebSocket):
    async with SessionLocal() as db:
        await validate_token(db, websocket.query_params.get('token')) 
        WechatClient_instance = await WechatClient.create(db, websocket.query_params.get('agent_uuid'))
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for response in WechatClient_instance.wechat_client(data):
            await websocket.send_text(response)
