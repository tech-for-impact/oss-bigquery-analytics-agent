from pathlib import Path
from pydantic_settings import BaseSettings
from app.src.utils.logger import logger

class Settings(BaseSettings):
    """Setting Configuration."""

    API_V1_STR: str = "/api"
    
    # LLM 제공자 설정
    LLM_PROVIDER: str = "openai"  # 기본값은 "azure", "openai"로 변경 가능
    
    # OpenAI 설정
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Azure OpenAI 설정
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str 
    AZURE_OPENAI_API_VERSION: str = "2025-03-01-preview"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o-mini"   

    # BigQuery 관련 설정
    BIGQUERY_API_URL: str = ""
    BIGQUERY_DATABASE: str
    GOOGLE_APPLICATION_CREDENTIALS: str 
    BIGQUERY_PROJECT_ID: str
    
    # 기타 설정
    CHAT_STEP_URL: str

    class Config:
        case_sensitive = False
        env_file = Path(__file__).parent.parent.parent / ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"LLM 제공자: {self.LLM_PROVIDER}")

    def get_current_llm_config(self):
        """현재 LLM 제공자에 따라 필요한 설정 반환"""
        if self.LLM_PROVIDER.lower() == "azure":
            return {
                "provider": "azure_openai",
                "api_key": self.AZURE_OPENAI_API_KEY,
                "endpoint": self.AZURE_OPENAI_ENDPOINT,
                "api_version": self.AZURE_OPENAI_API_VERSION,
                "deployment_name": self.AZURE_OPENAI_DEPLOYMENT_NAME
            }
        elif self.LLM_PROVIDER.lower() == "openai":  # openai
            return {
                "provider": "openai",
                "api_key": self.OPENAI_API_KEY,
                "model": self.OPENAI_MODEL
            }
        else:
            raise ValueError(f"지원하지 않는 LLM 제공자: {self.LLM_PROVIDER}")

settings = Settings() 