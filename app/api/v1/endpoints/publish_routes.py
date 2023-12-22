from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services.PublishServices.wechat_publish import WechatTemplate
from ....services.PublishServices.robot_publish import RobotTemplate
from ....services.PublishServices.website_publish import WebsiteTemplate
from ....schemas.publish_schema import PublishWechat
from ...dependencies import get_current_user


router = APIRouter()

# Generate wechat client
@router.post("/sapperchain/publish/wechat")
async def generate_wechat_client_endpoint(data: PublishWechat, db: AsyncSession = Depends(get_db_session), _: None = Depends(get_current_user)):
    WechatTemplate_Instance = await WechatTemplate.create(db)
    return await WechatTemplate_Instance.generate_client(data)

# Generate robot client
@router.post("/sapperchain/publish/robot")
async def generate_robot_client_endpoint(data: PublishWechat, db: AsyncSession = Depends(get_db_session), _: None = Depends(get_current_user)):
    RobotTemplate_Instance = await RobotTemplate.create(db)
    return await RobotTemplate_Instance.generate_client(data)

# Generate website client
@router.post("/sapperchain/publish/website")
async def generate_website_client_endpoint(data: PublishWechat, db: AsyncSession = Depends(get_db_session), _: None = Depends(get_current_user)):
    WebsiteTemplate_Instance = await WebsiteTemplate.create(db, data.agentUuid)
    return await WebsiteTemplate_Instance.generate_client(db)