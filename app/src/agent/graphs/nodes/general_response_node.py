from src.core.state import TextToSQLState
from src.core.model import Model
from src.core.model_manager import ModelManager

def general_response_node(state: TextToSQLState):
	llm = ModelManager.get_openai_model(Model.GPT_4O_MINI)
	last_message = state["messages"][-1]["content"]
	response = llm.invoke(f"일반 질문에 답변: {last_message}")
	return {"messages": [{"role": "assistant", "content": response.content}]}
	
	
	
	
	
	
	
	
	