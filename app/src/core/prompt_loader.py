from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, load_prompt, PromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate, FewShotPromptTemplate

PROMPT_DIR: Path = Path('app/prompts')


def load_fewshot_chat_prompt(prompt_name: str) -> FewShotPromptTemplate:
    """Few-shot 프롬프트를 로드합니다."""
    prompt_template = load_prompt(PROMPT_DIR / f"{prompt_name}.yml", encoding="utf-8")
    return prompt_template
    
    
def load_chat_prompt(prompt_name: str) -> PromptTemplate:
    """프롬프트를 로드합니다."""
    prompt_template = load_prompt(PROMPT_DIR / f"{prompt_name}.yml", encoding="utf-8")
    return prompt_template