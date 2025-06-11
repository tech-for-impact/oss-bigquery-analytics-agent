from src.core.model import Model
from src.core.model_config import get_openai_model
from src.prompt_templates.categorized import CategorizedPrompt
from src.core.prompt_template_manager import PromptTemplateManager
from langchain_core.output_parsers import StrOutputParser

def sql_or_chat_intent_chain(input_text: str) -> str:
	prompt_template: CategorizedPrompt = PromptTemplateManager.find_prompt_template("categorized")
	prompt = prompt_template.get_prompt()

	llm = get_openai_model(Model.GPT_4O_MINI)
	chain = prompt | llm | StrOutputParser()
	
	response = chain.invoke({"user_input": input_text})
	
	return response