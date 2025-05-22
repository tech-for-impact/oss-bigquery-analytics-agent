from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain_core.prompts import load_prompt, ChatPromptTemplate, MessagesPlaceholder
from pathlib import Path # Path 추가

from ..utils.llm.factory import LLMFactory # 수정된 경로

# 새 프로젝트 구조에 맞게 경로 수정
BASE_DIR = Path(__file__).parent.parent # src 디렉토리
PROMPT_DIR = BASE_DIR.parent / "prompts" # 수정된 프롬프트 경로

def create_classify_table_chain() -> Runnable:
    """테이블 분류를 위한 LangChain 체인 생성"""
    # TODO: LLMFactory.create 호출 시 provider를 settings에서 가져오도록 수정 고려
    llm = LLMFactory.create_from_settings(temperature=0.0) # create_from_settings 사용으로 변경

    prompt_path = PROMPT_DIR / "classify_table.yaml"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    classify_table_prompt = load_prompt(prompt_path, encoding="utf-8")

    chain = (
        ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="messages"),
            ("human", classify_table_prompt.template)])
        | llm 
        | StrOutputParser()
    )
    
    return chain 