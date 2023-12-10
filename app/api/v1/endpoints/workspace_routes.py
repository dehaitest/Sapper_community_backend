from fastapi import APIRouter, WebSocket, Depends, File, UploadFile
from ....services.WorkSpaceServices.require_to_splform import RequireToSPLForm
from ....services.WorkSpaceServices.splform_to_cfp import SPLFormToCFP
from ....services.WorkSpaceServices.splform_lint import SPLFormLint
from ....services.WorkSpaceServices.splform_copilot import SPLFormCopilot
from ....services.WorkSpaceServices.spl_compiler import SPLCompiler
from ....services.WorkSpaceServices.splform_emulator import SPLEmulator
from ....services.WorkSpaceServices.run_chain import RunChain
from ....services.WorkSpaceServices.upload_file import UploadUserFile
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....schemas.file_schema import FileResponse
from ....services.user_service import validate_token 
from ...dependencies import auth_current_user, get_current_user
import json

router = APIRouter()

# Initialize SPL form (deprecated)
@router.websocket("/ws/sapperchain/requiretosplform")
async def require_to_splform_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    requireToSPLForm_instance = await RequireToSPLForm.create(db)
    while True: 
        data = await websocket.receive_text()
        async for response in requireToSPLForm_instance.require_to_splForm(db, data):
            await websocket.send_text(response)

# SPL linting
@router.websocket("/ws/sapperchain/splformlint")
async def SPLForm_Lint_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    SPLFormLint_instance = await SPLFormLint.create(db, websocket.query_params.get('agent_uuid'))
    while True:
        data = await websocket.receive_text()
        async for response in SPLFormLint_instance.splform_lint(db):
            await websocket.send_text(response)

# SPL to Control Flow Path (CFP)
@router.websocket("/ws/sapperchain/splformtocfp")
async def splform_to_cfp_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    SPLFormToCFP_instance = await SPLFormToCFP.create(db, websocket.query_params.get('agent_uuid'))
    while True:
        data = await websocket.receive_text()
        async for response in SPLFormToCFP_instance.splform_to_cfp(db):
            await websocket.send_text(response)

# SPL form copilot
@router.websocket("/ws/sapperchain/formcopilot")
async def form_copilot_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    SPLFormCopilot_instance = await SPLFormCopilot.create(db, websocket.query_params.get('agent_uuid'))
    await websocket.send_text(json.dumps({'copilot': 'Welcome to Sapper copilot! How can I help you?'}))
    while True:
        data = await websocket.receive_text()
        async for response in SPLFormCopilot_instance.splform_copilot(db, data):
            await websocket.send_text(response)

# SPL compiler
@router.websocket("/ws/sapperchain/splcompiler")
async def spl_compiler_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    SPLCompiler_instance = await SPLCompiler.create(db, websocket.query_params.get('agent_uuid'))
    while True: 
        data = await websocket.receive_text()
        async for response in SPLCompiler_instance.spl_compiler(db):
            await websocket.send_text(response)

# SPL emulator
@router.websocket("/ws/sapperchain/splemulator")
async def spl_emulator_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    SPLEmulator_instance = await SPLEmulator.create(db, websocket.query_params.get('agent_uuid'))
    while True:
        data = await websocket.receive_text()
        async for response in SPLEmulator_instance.spl_emulator(data):
            await websocket.send_text(response)

# Run chain
@router.websocket("/ws/sapperchain/runchain")
async def run_chain_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db_session)):
    await validate_token(db, websocket.query_params.get('token'))
    await websocket.accept()
    RunChain_instance = await RunChain.create(db, websocket.query_params.get('agent_uuid'))
    step_mode = False  
    while True:
        data = await websocket.receive_text()
        if json.loads(data).get('mode') == "CONTINUE":
            step_mode = False
        elif json.loads(data).get('mode') == "RUN_NEXT":
            step_mode = True
        else:
            continue
        async for response in RunChain_instance.run_chain(data, step_mode):
            await websocket.send_text(response)
            if step_mode:
                break  

# Upload file
@router.post("/sapperchain/uploadfile", response_model=FileResponse)
async def upload_file_endpoint(file: UploadFile = File(...), db: AsyncSession = Depends(get_db_session), user_uuid = Depends(get_current_user)):
    UploadUserFile_Instance = await UploadUserFile.create(db, user_uuid)
    return await UploadUserFile_Instance.upload_user_file(file)