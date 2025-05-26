from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, load_prompt
from langchain_core.prompts import FewShotChatMessagePromptTemplate

PROMPT_DIR: Path = Path('app/src/prompts')


def load_fewshot_chat_prompt(prompt_name: str) -> FewShotChatMessagePromptTemplate:
    prompt_template = load_prompt(PROMPT_DIR / f"{prompt_name}.yaml", encoding="utf-8")
    return FewShotChatMessagePromptTemplate.from_messages([m.to_message() for m in prompt_template.messages])
    
    
def load_chat_prompt(prompt_name: str) -> ChatPromptTemplate:
    prompt_template = load_prompt(PROMPT_DIR / f"{prompt_name}.yaml", encoding="utf-8")
    return ChatPromptTemplate.from_messages([m.to_message() for m in prompt_template.messages])