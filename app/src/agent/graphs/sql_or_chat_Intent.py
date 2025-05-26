from src.prompt_templates.categorized import CategoriedPrompt
from src.core.prompt_template_manager import PromptTemplateManager

def sql_or_chat_intent_chain(input_text: str) -> str:
	prompt_template: CategoriedPrompt = PromptTemplateManager.get_template("categorized")
	prompt = prompt_template.get_prompt(user_input=input_text)
	
	return prompt