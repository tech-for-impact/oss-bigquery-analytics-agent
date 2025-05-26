# ./src/agent/webapp.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.prompt_template_manager import PromptTemplateManager
from src.core.prompt_template_registry import PromptTemplateRegistry
from src.agent.routers.health_check_router import router as health_check_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    PromptTemplateManager.load_all_templates("src.prompt_templates")
    loaded = list(PromptTemplateRegistry.get_registry().keys())
    print(f"Loaded prompts: {loaded}")
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)
app.include_router(health_check_router)

# ... can add custom routes if needed.