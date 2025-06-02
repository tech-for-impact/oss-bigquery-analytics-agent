# ./src/agent/webapp.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.prompt_template_manager import PromptTemplateManager
from src.agent.routers.chat_router import router as chat_router
from src.agent.routers.health_check_router import router as health_check_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await PromptTemplateManager.init_prompt_registry()
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)
app.include_router(health_check_router)
app.include_router(chat_router)

# Enable debug mode for langchain
from langchain.globals import set_debug
set_debug(True)

# ... can add custom routes if needed.