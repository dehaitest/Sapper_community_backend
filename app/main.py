from fastapi import FastAPI
from .api.v1.endpoints import websocket_routes
from .core.config import settings
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_routes.router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/", StaticFiles(directory="app/templates", html=True), name="templates")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)