from fastapi.responses import FileResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    return FileResponse('app/static/favicon.ico')
