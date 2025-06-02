from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Any, Dict

from src.agent.schemas.chat_request import ChatRequest
from src.agent.graphs.sql_or_chat_Intent import sql_or_chat_intent_chain

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

@router.post("/sql-chat-intent", response_model=SqlChatIntentResponse)
def sql_chat_intent(request: ChatRequest) -> SqlChatIntentResponse:
	answer = sql_or_chat_intent_chain(request.input)

	return SqlChatIntentResponse(
		status="ok",
		message="success",
		data={
			"intent": "sql_chat_intent",
			"input": request.input,
			"output": answer,
		}
	)
