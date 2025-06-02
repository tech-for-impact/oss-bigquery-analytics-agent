import asyncio
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, load_prompt, PromptTemplate, FewShotPromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate
from langchain_core.messages import HumanMessage

# 현재 파일의 위치를 기준으로 프로젝트 루트를 찾고, 거기서 app/prompts로 이동
PROMPT_DIR: Path = Path(__file__).parent.parent.parent / 'prompts'


async def load_fewshot_chat_prompt(prompt_name: str) -> str:
    """비동기적으로 few-shot 예시들을 로드하여 포맷팅된 문자열로 반환합니다."""
    prompt_template = await asyncio.to_thread(
        load_prompt, 
        PROMPT_DIR / f"{prompt_name}.yaml", 
        encoding="utf-8"
    )
    
    # FewShotPromptTemplate에서 예시들을 추출하여 문자열로 포맷팅
    if isinstance(prompt_template, FewShotPromptTemplate):
        formatted_examples = []
        
        # prefix가 있으면 추가
        if prompt_template.prefix:
            formatted_examples.append(prompt_template.prefix.strip())
        
        # 각 예시를 포맷팅
        for example in prompt_template.examples:
            # example_prompt를 사용하여 각 예시를 포맷팅
            formatted_example = prompt_template.example_prompt.format(**example)
            formatted_examples.append(formatted_example)
        
        return "\n\n".join(formatted_examples)
    else:
        return ""
    
    
async def load_chat_prompt(prompt_name: str) -> PromptTemplate:
    """비동기적으로 프롬프트를 로드합니다."""
    prompt_template = await asyncio.to_thread(
        load_prompt, 
        PROMPT_DIR / f"{prompt_name}.yaml", 
        encoding="utf-8"
    )
    
    # PromptTemplate을 그대로 반환 (ChatPromptTemplate 변환 안함)
    return prompt_template