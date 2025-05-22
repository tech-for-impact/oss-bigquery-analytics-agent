from typing import Dict, Any, Union, List

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage

from ..utils.logger import logger
from .graph import create_graph_chain

def create_chat_chain() -> RunnableLambda:
    """
    챗봇 체인 생성 (chat.py 스타일, 버전 없음)
    주어진 입력에 대해 전체 그래프 워크플로우를 실행합니다.
    """
    #멀티턴을 적용할때 필요한 메시지타입.
    def convert_to_message_type(msg_dict: Dict[str, Any]) -> Union[HumanMessage, AIMessage]:
        msg_type = msg_dict.get("type", "")
        content = msg_dict.get("content", "")

        if msg_type == "human":
            return HumanMessage(content=content)
        elif msg_type == "ai":
            return AIMessage(content=content)
        else:
            logger.error(f"Unknown message type: {msg_type} in convert_to_message_type. Original dict: {msg_dict}")
            raise ValueError(f"Unknown message type: {msg_type}")

    def convert_messages(input_dict: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Input to convert_messages: {str(input_dict)}")
        
        messages_input = input_dict.get("messages", [])
        if not isinstance(messages_input, list):
            logger.warning(f"'messages' field is not a list: {messages_input}. Using empty list.")
            messages_input = []

        # chat.py는 messages[-1:]를 사용하나, graph는 전체 히스토리를 기대할 수 있음.
        # 사용자 요청 "chat.py와 같게"에 따라 messages[-1:] 사용.
        messages_for_state = []
        if messages_input:
            last_message = messages_input[-1]
            if isinstance(last_message, dict):
                messages_for_state.append(convert_to_message_type(last_message))
            elif hasattr(last_message, 'type') and hasattr(last_message, 'content'): # 이미 Message 객체인 경우
                messages_for_state.append(last_message)


        chat_id = input_dict.get("chat_id", "")
        org_table_name = input_dict.get("org_table_name", "medium_sample")

        state = {
            "messages": messages_for_state,
            "org_table_name": org_table_name,
            "chat_id": chat_id,
            "SQLquery": None, # GraphState의 다른 필드 초기화
            "answer": None,
            "state": None,
        }
        logger.info(f"Converted state for graph: {state}")
        return state

    graph = create_graph_chain()

    async def run_chain(input_data: Dict[str, Any]) -> str:
        state = convert_messages(input_data)
        # graph.ainvoke는 전체 GraphState를 반환.
        # 최종 답변은 result_state.get("answer")로 추출.
        result_state = await graph.ainvoke(state) 
        answer = result_state.get("answer", "") 
        logger.info(f"Answer from graph: {answer}")
        return answer

    return RunnableLambda(run_chain) 