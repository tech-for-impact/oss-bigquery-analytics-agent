from src.core.custom_base_template import CustomBaseTemplate
from src.core.prompt_loader import load_chat_prompt, load_fewshot_chat_prompt
from langchain_core.prompts import BasePromptTemplate

class CategoriedPrompt(CustomBaseTemplate):

	def __init__(self):
		self.prompt_name = "categorized"
		self.fewshot_prompt_name = "categorized_fewshot"
		self.template = self.build()
		
    
	def build(self) -> BasePromptTemplate:
		chat_prompt = load_chat_prompt(self.prompt_name)
		fewshot_prompt = load_fewshot_chat_prompt(self.fewshot_prompt_name)
		return chat_prompt.partial(fewshot_prompt=fewshot_prompt)
	
	def get_prompt(self, **kwargs) -> str:
		return self.template.format(**kwargs)