from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict

from src.agent.schemas.chat_request import ChatRequest
from src.agent.graphs.text_to_sql_graph import text_to_sql_graph

router = APIRouter()
router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)

class SqlChatIntentResponse(BaseModel):
	status: str
	message: str
	data: Dict[str, Any]

@router.post("/invoke", response_model=SqlChatIntentResponse)
def invoke(request: ChatRequest) -> SqlChatIntentResponse:
	answer = text_to_sql_graph(request.input)
	output = answer.get("messages", [])[-1]["content"]

	return SqlChatIntentResponse(
		status="ok",
		message="success",
		data={
			"input": request.input,
			"output": output,
		}
	)
