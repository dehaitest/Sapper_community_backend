from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services import prompt_service
from ....schemas.prompt_schema import PromptCreate, PromptUpdate, PromptResponse
from ...dependencies import auth_current_user
from typing import List

router = APIRouter()

# Create prompt
@router.post("/prompts/", response_model=PromptResponse)
async def create_prompt_endpoint(prompt_data: PromptCreate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    return await prompt_service.create_prompt(db, prompt_data.model_dump())

# Edit prompt
@router.put("/prompts/{prompt_id}", response_model=PromptResponse)
async def edit_prompt_endpoint(prompt_id: int, update_data: PromptUpdate, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    prompt = await prompt_service.edit_prompt(db, prompt_id, update_data.model_dump())
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt

# Get prompt by name
@router.get("/prompts/by-name/", response_model=PromptResponse)
async def get_prompt_by_name_endpoint(prompt_name: str = Query(...), db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    prompt = await prompt_service.get_prompt_by_name(db, prompt_name)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt

# Get prompt by id
@router.get("/prompts/by-id/{prompt_id}", response_model=PromptResponse)
async def get_prompt_by_id_endpoint(prompt_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    print('byid')
    prompt = await prompt_service.get_prompt_by_id(db, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt

# Delete prompt
@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt_endpoint(prompt_id: int, db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    success = await prompt_service.delete_prompt(db, prompt_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    
# Get all prompt
@router.get("/prompts/all", response_model=List[PromptResponse])
async def get_all_prompts_endpoint(db: AsyncSession = Depends(get_db_session), _: None = Depends(auth_current_user)):
    prompts = await prompt_service.get_all_prompts(db)
    return prompts
