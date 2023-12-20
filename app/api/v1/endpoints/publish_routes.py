from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services.PublishServices.wechat import WechatTemplate
from ....services.PublishServices.robot import RobotTemplate
from ....schemas.publish_schema import PublishWechat


router = APIRouter()

# Generate wechat client
@router.post("/sapperchain/publish/wechat")
async def generate_wechat_client_endpoint(data: PublishWechat, db: AsyncSession = Depends(get_db_session)):
    WechatTemplate_Instance = await WechatTemplate.create(db)
    return await WechatTemplate_Instance.generate_client(data)

# Generate robot client
@router.post("/sapperchain/publish/robot")
async def generate_wechat_client_endpoint(data: PublishWechat, db: AsyncSession = Depends(get_db_session)):
    RobotTemplate_Instance = await RobotTemplate.create(db)
    return await RobotTemplate_Instance.generate_client(data)