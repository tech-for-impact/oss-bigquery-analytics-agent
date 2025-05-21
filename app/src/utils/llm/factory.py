import os
from typing import Literal, Optional, Dict, Any

from langchain.chat_models.base import BaseChatModel
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from app.src.core.settings import settings
from app.src.utils.logger import logger

# 제공자 타입 정의
ProviderType = Literal["azure_openai", "openai"]

"""
LLM 팩토리 모듈

이 모듈은 다양한 LLM(Large Language Model) 제공자의 인스턴스를 생성하는 팩토리 패턴을 구현합니다.

지원되는 제공자:
- Azure OpenAI: GPT 모델 시리즈 (기본값: gpt-4o-mini)
- OpenAI: GPT 모델 시리즈 (기본값: gpt-4o-mini)

각 제공자별로 모델, 온도 등의 파라미터를 설정할 수 있으며,
적절한 API 키가 환경 변수를 통해 제공되어야 합니다.
"""

class LLMFactory:
    """LLM 인스턴스를 생성하는 팩토리 클래스"""
    
    @staticmethod
    def create(
        provider: Optional[ProviderType] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        streaming: bool = False,
    ) -> BaseChatModel:
        """지정된 공급자와 모델을 사용하여 LLM 인스턴스를 생성합니다."""
        if provider == "azure_openai":
            return AzureChatOpenAI(
                deployment_name=model or settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                openai_api_version=settings.AZURE_OPENAI_API_VERSION,
                openai_api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                temperature=temperature,
                streaming=streaming,
            )
        elif provider == "openai":
            return ChatOpenAI(
                model=model or settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=temperature,
                streaming=streaming,
            )
        else:
            raise ValueError(f"지원하지 않는 provider: {provider}")
            
    @staticmethod
    def create_from_settings(
        temperature: float = 0.0,
        streaming: bool = False,
        model: Optional[str] = None,
    ) -> BaseChatModel:
        """settings에 설정된 현재 LLM 제공자를 사용하여 인스턴스 생성"""
        llm_config = settings.get_current_llm_config()
        provider = llm_config["provider"]
        model_key = "model" if provider == "openai" else "deployment_name"
        model_name = model or llm_config.get(model_key)

        logger.info(f"LLM 인스턴스 생성: provider={provider}, model={model_name}")

        return LLMFactory.create(
            provider=provider,
            model=model_name,
            temperature=temperature,
            streaming=streaming,
        ) 