from fastapi import APIRouter, WebSocket, Depends
from ....services.WorkSpaceServices.require_to_splform import RequireToSPLForm
from ....services.WorkSpaceServices.splform_to_nl import SPLFormToNL
from ....services.WorkSpaceServices.nl_to_splform import NLToSPLForm
from ....services.WorkSpaceServices.splform_copilot import SPLFormCopilot
from ....services.WorkSpaceServices.spl_compiler import SPLCompiler
from ....services.WorkSpaceServices.splform_emulator import SPLEmulator
from ....services.WorkSpaceServices.run_chain import RunChain
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session

router = APIRouter()

# Initialize SPL form
@router.websocket("/ws/sapperchain/requiretosplform")
async def require_to_splform_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    requireToSPLForm_instance = await RequireToSPLForm.create(db, data)
    async for response in requireToSPLForm_instance.require_to_splForm(db):
        await websocket.send_text(response)

# Natural language to SPL form
@router.websocket("/ws/sapperchain/nltosplform")
async def NLText_to_SPLForm_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    NLToSPLForm_instance = await NLToSPLForm.create(db)
    async for response in NLToSPLForm_instance.nl_to_splform(db, data):
        await websocket.send_text(response)

# SPL form to natural lanuage
@router.websocket("/ws/sapperchain/splformtonl")
async def splform_to_nl_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    SPLFormToNL_instance = await SPLFormToNL.create(db)
    async for response in SPLFormToNL_instance.splform_to_nl(db, data):
        await websocket.send_text(response)

# SPL form copilot
@router.websocket("/ws/sapperchain/formcopilot")
async def form_copilot_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    SPLFormCopilot_instance = await SPLFormCopilot.create(db)
    while True:
        data = await websocket.receive_text()
        async for response in SPLFormCopilot_instance.splform_copilot(db, data):
            await websocket.send_text(response)

# SPL compiler
@router.websocket("/ws/sapperchain/splcompiler")
async def spl_compiler_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    SPLCompiler_instance = await SPLCompiler.create(db)
    async for response in SPLCompiler_instance.spl_compiler(db, data):
        await websocket.send_text(response)

# SPL emulator
@router.websocket("/ws/sapperchain/splemulator")
async def spl_emulator_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    SPLEmulator_instance = await SPLEmulator.create(db, data)
    while True:
        data = await websocket.receive_text()
        async for response in SPLEmulator_instance.spl_emulator(data):
            await websocket.send_text(response)

# Run chain
@router.websocket("/ws/sapperchain/runchain")
async def run_chain_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_text()
    RunChain_instance = await RunChain.create(db, data)
    while True:
        data = await websocket.receive_text()
        async for response in RunChain_instance.run_chain(data):
            await websocket.send_text(response)