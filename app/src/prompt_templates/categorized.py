from src.core.custom_base_template import CustomBaseTemplate
from src.core.prompt_loader import load_chat_prompt
from langchain_core.prompts import BasePromptTemplate

class CategorizedPrompt(CustomBaseTemplate):

    def __init__(self):
        self.prompt_name = "categorized"
        self.template = self.build()
        
    def build(self) -> BasePromptTemplate:
        """
        BasePromptTemplate을 구성합니다.
        
        Returns:
            BasePromptTemplate: 구성된 프롬프트 템플릿
        """
        # 프롬프트 로딩 (few-shot 없이)
        chat_prompt = load_chat_prompt(self.prompt_name)
        return chat_prompt
    
    def get_prompt(self, user_input: str, **kwargs) -> str:
        """
        사용자 입력을 받아 최종 프롬프트를 문자열로 반환합니다.
        
        Args:
            user_input (str): 사용자 입력 텍스트
            **kwargs: 추가 템플릿 변수
            
        Returns:
            str: 포맷된 프롬프트 문자열
        """
        # PromptTemplate의 format 메서드 사용
        return self.template.format(user_input=user_input, **kwargs) 