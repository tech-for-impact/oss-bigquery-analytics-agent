from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict
from typing import Optional
from typing_extensions import Annotated
import operator

class TextToSQLState(TypedDict):
    """State for the agent's conversation and processing."""
    messages: Annotated[list[AnyMessage], operator.add] # 대화 기록
    schema: Optional[str] # 스키마 정보
    sql_query: Optional[str]    # 실행 쿼리
    query_result: Optional[dict]  # 쿼리 결과
    error: Optional[str]  # 에러 메시지