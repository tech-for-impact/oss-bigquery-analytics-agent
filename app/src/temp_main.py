from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# workflows.sql_chain에서 create_chat_chain 임포트 (경로 수정)
from .workflows.sql_chain import create_chat_chain 
from .utils.logger import logger # 로거 추가

# 요청 본문을 위한 Pydantic 모델 정의
class ChatMessageInput(BaseModel):
    type: str
    content: str

# 새로운 'input' 필드 모델 정의
class InputPayload(BaseModel):
    messages: List[ChatMessageInput]
    org_table_name: Optional[str] = "medium_sample"
    chat_id: Optional[str] = "" # 명세에 따라 기본값을 빈 문자열로 설정

# 전체 요청 모델 (기존 ChatAPIRequest 대체)
class LangserveChatAPIRequest(BaseModel):
    input: InputPayload
    config: Optional[Dict[str, Any]] = {}
    kwargs: Optional[Dict[str, Any]] = {}

class ChatAPIResponse(BaseModel):
    answer: str

app = FastAPI(
    title="OSS BigQuery Analytics Agent API - Chat",
    description="API for a conversational agent powered by BigQuery analytics.",
    version="0.1.0" # 이전 버전에서 업데이트되었으므로 버전 변경
)


chat_chain_runnable = create_chat_chain()

@app.post("/api/chat", response_model=ChatAPIResponse, tags=["Conversational Agent"])
async def handle_chat_request(request: LangserveChatAPIRequest): # 요청 모델 변경
    logger.info(f"Received chat request: {request.model_dump_json()}")
    try:
        # 체인에 전달할 데이터는 request.input 에서 가져옴
        input_data_for_chain = {
            "messages": [msg.model_dump() for msg in request.input.messages], # Pydantic 모델을 dict로 변환
            "chat_id": request.input.chat_id,
            "org_table_name": request.input.org_table_name
        }
        
        # chat_chain_runnable은 RunnableLambda이므로 직접 호출
        # config나 kwargs를 체인에 전달해야 한다면 이 부분에서 추가 처리 필요
        # 현재 create_chat_chain은 config나 kwargs를 명시적으로 사용하지 않으므로 input_data_for_chain만 전달
        response_content = await chat_chain_runnable.ainvoke(input_data_for_chain)
        
        return ChatAPIResponse(answer=response_content)
    except ValueError as ve:
        logger.error(f"ValueError in chat endpoint: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 서버 실행을 위한 uvicorn 명령어 (참고용)
# uvicorn oss-bigquery-analytics-agent.app.src.main:app --reload --host 0.0.0.0 --port 8000 