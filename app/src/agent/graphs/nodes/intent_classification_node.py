from src.core.state import TextToSQLState
from src.core.model import Model
from src.core.model_manager import ModelManager
from src.prompt_templates.categorized import CategorizedPrompt
from src.core.prompt_template_manager import PromptTemplateManager
from langchain_core.output_parsers import StrOutputParser

def intent_classification_node(state: TextToSQLState) -> dict:
	input_text = state["messages"][-1]["content"]
	prompt_template: CategorizedPrompt = PromptTemplateManager.find_prompt_template("categorized")
	prompt = prompt_template.get_prompt()

	llm = ModelManager.get_openai_model(Model.GPT_4O_MINI)

	chain = prompt | llm | StrOutputParser()
	
	analysis_response = chain.invoke({"user_input": input_text})

	# SQL_QUERY or GENERAL or AGGREGATE_QUERY
	intent = analysis_response.strip() if analysis_response.strip() in ["SIMPLE_QUERY","AGGREGATE_QUERY", "GENERAL"] else "GENERAL"
	
	return {
		"intent": intent
	}






	
	
