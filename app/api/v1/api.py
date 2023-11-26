# app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import user_routes, websocket_routes, workspace_routes, static_routes

api_router = APIRouter()
api_router.include_router(static_routes.router, tags=["static"])
api_router.include_router(user_routes.router, tags=["users"])
api_router.include_router(websocket_routes.router, tags=["chatbot"])
api_router.include_router(websocket_routes.router, tags=["workspace"])
# Include other routers as needed
