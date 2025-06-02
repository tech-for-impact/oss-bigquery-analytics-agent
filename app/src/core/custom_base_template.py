from abc import ABC, abstractmethod
from langchain_core.prompts import BasePromptTemplate
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage

class CustomBaseTemplate(ABC):
    """
    모든 프롬프트 템플릿은 이 클래스를 상속해야 합니다.
    `prompt_name` 과 `template` (BasePromptTemplate 인스턴스)을 정의하고,
    `build()` 메서드로 최종 PromptTemplate을 구성해야 합니다.
    """

    prompt_name: str
    template: BasePromptTemplate
    

    @abstractmethod
    def build(self) -> BasePromptTemplate:
        """
        구체적인 PromptTemplate을 구성해 반환합니다.
        """
        ...
    
    @abstractmethod
    def get_prompt(self, **kwargs) -> str:
        """
        최종 PromptTemplate을 문자열로 반환합니다.
        기본 구현을 제공하되, 하위 클래스에서 오버라이드 가능합니다.
        
        Args:
            **kwargs: 사용자 입력, few-shot 예시 등 템플릿 변수
            
        Returns:
            str: 포맷된 프롬프트 문자열
        """
        messages = self.get_prompt(**kwargs)
        return "\n".join([msg.content for msg in messages if hasattr(msg, 'content')])
    
