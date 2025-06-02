from src.core.custom_base_template import CustomBaseTemplate
from src.core.prompt_loader import load_fewshot_chat_prompt
from langchain_core.prompts import BasePromptTemplate

class CategorizedFewShotPrompt(CustomBaseTemplate):

    def __init__(self):
        self.prompt_name = "categorized_few_shot"
        self.template = self.build()
        
    def build(self) -> BasePromptTemplate:
        """
        BasePromptTemplate을 구성합니다 (Few-shot 방식).
        
        Returns:
            BasePromptTemplate: 구성된 Few-shot 프롬프트 템플릿
        """
        # Few-shot 프롬프트 로딩
        fewshot_prompt = load_fewshot_chat_prompt(self.prompt_name)
        return fewshot_prompt
    
    def get_prompt(self, user_input: str, **kwargs) -> str:
        """
        사용자 입력을 받아 최종 프롬프트를 문자열로 반환합니다.
        
        Args:
            user_input (str): 사용자 입력 텍스트
            **kwargs: 추가 템플릿 변수
            
        Returns:
            str: 포맷된 프롬프트 문자열
        """
        # FewShotPromptTemplate의 format 메서드 사용
        # user_input을 새로운 질문으로 추가
        formatted_examples = self.template.format(**kwargs)
        
        # 사용자 입력을 마지막에 추가
        final_prompt = f"{formatted_examples}\n\n사용자: {user_input}\nAI:"
        
        return final_prompt 