from src.core.custom_base_template import CustomBaseTemplate
from src.core.prompt_loader import load_chat_prompt, load_fewshot_chat_prompt
from langchain_core.prompts import BasePromptTemplate, PromptTemplate

class CategorizedPrompt(CustomBaseTemplate):

	def __init__(self):
		self.prompt_name = "categorized"
		self.fewshot_prompt_name = "categorized_few_shot"
		# template은 _async_init에서 설정됨
		
    
	async def build(self) -> PromptTemplate:
		chat_prompt = await load_chat_prompt(self.prompt_name)
		fewshot_examples = await load_fewshot_chat_prompt(self.fewshot_prompt_name)
		return chat_prompt.partial(few_shot_examples=fewshot_examples)
	
	def get_prompt(self, user_input: str) -> str:
		# format_messages() 대신 format()을 사용하여 문자열을 반환
		return self.template.format(user_input=user_input)