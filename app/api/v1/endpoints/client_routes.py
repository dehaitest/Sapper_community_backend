from fastapi import APIRouter, WebSocket, Depends, Query
from ....services.chat_service import ChatService
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services.database import SessionLocal
from ....services.user_service import validate_token 
from ....services.ClientServices.wechat_client import WechatClient
from ....services.ClientServices.website_client import WebsiteClient
from ....schemas.client_schema import ClientWebsite

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

# Website client
@router.post("/client/website")
async def website_client_endpoint(data: ClientWebsite, agent_uuid: str = Query(...), instruction: str = Query(...), db: AsyncSession = Depends(get_db_session)):
    WebsiteClient_Instance = await WebsiteClient.create(db, agent_uuid, instruction)
    return await WebsiteClient_Instance.website_client(data)