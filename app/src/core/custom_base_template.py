from abc import ABC, abstractmethod
from langchain_core.prompts import BasePromptTemplate

class CustomBaseTemplate(ABC):
    """
    모든 프롬프트 템플릿은 이 클래스를 상속해야 합니다.
    `prompt_name` 과 `template` (BasePromptTemplate 인스턴스)을 정의하고,
    `build()` 메서드로 최종 PromptTemplate을 구성해야 합니다.
    """
    prompt_name: str
    template: BasePromptTemplate

    @classmethod
    async def create(cls):
        """비동기 팩토리 메서드 - 인스턴스를 생성하고 초기화합니다."""
        instance = cls()
        await instance._async_init()
        return instance

    async def _async_init(self):
        """비동기 초기화 메서드 - 서브클래스에서 필요시 오버라이드합니다."""
        self.template = await self.build()

    @abstractmethod
    async def build(self) -> BasePromptTemplate:
        """
        구체적인 PromptTemplate을 구성해 반환합니다.
        """
        ...
    
    @abstractmethod
    def get_prompt(self, **kwargs) -> str:
        """
        최종 PromptTemplate을 문자열로 반환합니다.
        **kwargs: 사용자 입력, few-shot 예시 등 템플릿 변수
        """
        ...