# app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import agent_routes, user_routes, websocket_routes, workspace_routes, static_routes, prompt_management_routes, settings_routes, publish_routes

api_router = APIRouter()
api_router.include_router(static_routes.router, tags=["static"])
api_router.include_router(user_routes.router, tags=["users"])
api_router.include_router(settings_routes.router, tags=["settings"])
api_router.include_router(websocket_routes.router, tags=["chatbot"])
api_router.include_router(prompt_management_routes.router, tags=["prompt management"])
api_router.include_router(agent_routes.router, tags=["agent management"])
api_router.include_router(workspace_routes.router, tags=["workspace"])
api_router.include_router(publish_routes.router, tags=["publish"])

