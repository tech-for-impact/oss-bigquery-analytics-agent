from langchain_community.chat_models import ChatOpenAI
from src.core.model import Model
import os

class ModelManager:
    # LangChain 0.3.25 기준으로 ChatOpenAI를 사용한다고 가정합니다.
    # 환경변수 OPENAI_API_KEY가 설정되어 있어야 합니다.
    @staticmethod
    def get_openai_model(model: Model):
        """
        LangChain ChatOpenAI 모델 인스턴스를 반환합니다.
        필요에 따라 model_name, temperature 등 설정을 변경하세요.
        """
        return ChatOpenAI(
            model=model.value,
            temperature=0.7,
            api_key=ModelManager._load_openai_api_key()
        )

    @staticmethod
    def _load_openai_api_key() -> str:
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("OPENAI_API_KEY is not set")

        return os.getenv("OPENAI_API_KEY")