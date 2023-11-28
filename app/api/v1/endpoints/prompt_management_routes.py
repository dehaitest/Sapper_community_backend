from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.database import get_db_session
from ....services.prompt_service import create_prompt, edit_prompt, select_prompt_by_name, delete_prompt, get_all_prompts, select_prompt_by_id
from ....schemas.prompt_schema import PromptCreate, PromptUpdate, PromptResponse
from typing import List

router = APIRouter()

@router.post("/prompts/", response_model=PromptResponse)
async def create_prompt_endpoint(prompt_data: PromptCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_prompt(db, prompt_data.model_dump())

@router.put("/prompts/{prompt_id}", response_model=PromptResponse)
async def edit_prompt_endpoint(prompt_id: int, update_data: PromptUpdate, db: AsyncSession = Depends(get_db_session)):
    prompt = await edit_prompt(db, prompt_id, update_data.model_dump())
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.get("/prompts/by-name/", response_model=PromptResponse)
async def get_prompt_by_name_endpoint(prompt_name: str, db: AsyncSession = Depends(get_db_session)):
    prompt = await select_prompt_by_name(db, prompt_name)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.get("/prompts/by-id/{prompt_id}", response_model=PromptResponse)
async def get_prompt_by_id_endpoint(prompt_id: int, db: AsyncSession = Depends(get_db_session)):
    print('byid')
    prompt = await select_prompt_by_id(db, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt_endpoint(prompt_id: int, db: AsyncSession = Depends(get_db_session)):
    success = await delete_prompt(db, prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
@router.get("/prompts/all", response_model=List[PromptResponse])
async def get_all_prompts_endpoint(db: AsyncSession = Depends(get_db_session)):
    prompts = await get_all_prompts(db)
    return prompts
