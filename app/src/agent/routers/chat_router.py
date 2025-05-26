from fastapi import APIRouter, Request

from src.agent.graphs.sql_or_chat_Intent import sql_or_chat_intent_chain

router = APIRouter()
router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sql-chat-intent")
def sql_chat_intent(request: Request) -> str:
	answer = sql_or_chat_intent_chain(request.input)

	return {
		"status": "ok",
		"message": "success",
		"data": {
			"intent": "sql_chat_intent",
			"input": request.input,
			"output": answer,
		}
	}
