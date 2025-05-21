from typing import List, Union, Dict
from typing_extensions import TypedDict, Optional
from pathlib import Path # pathlib.Path를 직접 사용하도록 수정
from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, load_prompt
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langgraph.graph import END, StateGraph

# 새 프로젝트 구조에 맞게 경로 수정
from ..utils.llm.factory import LLMFactory # 수정된 경로
# from .sql_chain import create_sql_chain # 순환 참조 방지를 위해 주석 처리
from datetime import datetime

from ..utils.logger import logger # 수정된 경로
from ..utils.date_utils import format_date, check_query_date # 수정된 경로

# 새 프로젝트 구조에 맞게 경로 수정
PROMPT_DIR = Path(__file__).parent.parent.parent / "prompts" # graph.py 위치에서 app/prompts 를 상대경로로 지정
llm = LLMFactory.create_from_settings(temperature=0.0)

class GraphState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]
    org_table_name: Optional[str]
    state: Optional[str]
    SQLquery: Optional[str]
    chat_id: Optional[str] # chat_id는 report 생성 시 사용되었으나, 다른 용도로 사용될 수 있으므로 유지
    answer: Optional[str] # SQL 쿼리 또는 최종 답변을 저장

def get_full_input(state: GraphState) -> str:
    messages_contents = [f"{'HumanMessage' if m.type == 'human' else 'AIMessage'}: {m.content}" for m in state["messages"]]
    return "\\n".join(messages_contents)

def get_latest_input(state: GraphState) -> str:
    if len(state["messages"]) > 0 and state["messages"][-1].type == "human":
        return state["messages"][-1].content
    return ""

def categorized(state: GraphState) -> GraphState:
    state["state"] = "categorized"
    state["answer"] = ""
    state["SQLquery"] = ""
    logger.info(f"MessageHistory : {state['messages']}")
    user_prompt = load_prompt(PROMPT_DIR / "categorized.yaml", encoding="utf-8")
    prompt_template = ChatPromptTemplate.from_messages([
        ("placeholder", "{messages}"),
        ("human", user_prompt.format(input="{input}"))
    ])
    chain = prompt_template | llm | StrOutputParser()
    try:
        response = chain.invoke({
            "messages": state["messages"][:-1] if len(state["messages"]) > 1 else [],
            "input": state["messages"][-1].content
        })
        result = response.strip()
        classification_map = {
            "block": ("block", "block으로 분류"),
            "out_of_scope": ("out_of_scope", "out_of_scope 로 분류"),
            "SQLquery": ("SQLquery", "쿼리문 생성으로 분류"),
        }
        logger.info(f"categorized : {result}")
        if result in classification_map:
            state["state"], state["answer"] = classification_map[result]
        else:
            state["state"] = "roll_base_answer"
            state["answer"] = f"알 수 없는 분류 결과 {result}"
    except Exception as e:
        print(f"Classification error: {str(e)}")
        state["state"] = "roll_base_answer"
        state["answer"] = "응답을 생성할 수 없습니다."
    return state

def roll_base_answer(state: GraphState) -> GraphState:
    """
    block, out_of_scope, 기타(unknown) 상황에서 안내 메시지 반환.
    """
    if state["state"] == "block":
        state["answer"] = "🚫 앗! 서비스 이용 중 부적절한 표현이 감지되었어요. 데이터를 분석하는 질문을 입력해 주시면, 더 좋은 답변을 드릴게요!"
    elif state["state"] == "out_of_scope":
        state["answer"] = "😅 제가 아는 분야가 아니에요! 저는 후원 데이터 분석 전문가랍니다!\n예: '지난주 youtube / video 채널의 방문자 수 알려줘' 같은 질문을 해보세요!"
    elif state["state"] == "out_of_date":
        state["answer"] = "🗓️ 데이터 조회는 2024.01.01부터 가능합니다."
    else:
        state["answer"] = "앗! 생각하는 도중에 문제가 생겼어요. 데이터 분석을 요구하는 질문으로 요청해주시면 잘 생각해서 답변 드릴게요!"
    
    logger.info(f"roll_base_answer : answer=\"{state['answer']}\", messages=\"{state['messages']}\"")
    return state

def missing_data_answer(state: GraphState) -> GraphState:
    state["state"] = "missing_data_answer"
    prompt = load_prompt(PROMPT_DIR / "missing_data.yaml", encoding="utf-8")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "input": state["messages"][-1].content,
        "messages": state["messages"][:-1] if len(state["messages"]) > 1 else []
    })
    state["answer"] = response
    logger.info(f"missing_data_answer : {state['answer']}")
    return state

def judged_sql_query(state: GraphState) -> GraphState:
    state["state"] = "judged_sql_query"
    prompt = load_prompt(PROMPT_DIR / "judge_sql_or_end.yaml", encoding="utf-8")
    chat_prompt = ChatPromptTemplate.from_messages([
        ("placeholder", "{messages}"),
        ("human", prompt.format(input="{input}"))
    ])
    chain = chat_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "messages": state["messages"][:-1] if len(state["messages"]) > 1 else [],
        "input": state["messages"][-1].content
    })
    answer = response.strip().lower()
    if answer == "true":
        state["answer"] = "True"
    else:
        state["answer"] = "False"
    logger.info(f"judged_sql_query : {answer}")
    return state

def transfer_date(state: GraphState) -> GraphState:
    state["state"] = "transfer_date"
    current_date = format_date(datetime.now())
    user_query = get_latest_input(state)
    is_valid_date = check_query_date(user_query)
    if not is_valid_date:
        state["state"] = "out_of_date"
        return state
    prompt_template = load_prompt(PROMPT_DIR / "rewrite_question.yaml", encoding="utf-8")
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({
        "input": get_latest_input(state),
        "current_date": current_date,
        "messages": state["messages"][:-1] if len(state["messages"]) > 1 else []
    })
    state["messages"][-1].content = response
    is_valid_date_after = check_query_date(response)
    if not is_valid_date_after:
        state["state"] = "out_of_date"
        return state
    logger.info(f"transfer_date : {response}")
    return state

def transfer_TextToSQL(state: GraphState) -> GraphState:
    state["state"] = "transfer_TextToSQL"
    
    llm = LLMFactory.create_from_settings(temperature=0.0)

    # 프롬프트 로드
    system_prompt = load_prompt(PROMPT_DIR / "text2sql_system.yaml", encoding="utf-8").template
    user_prompt = load_prompt(PROMPT_DIR / "text2sql_user.yaml", encoding="utf-8").template

    chain = (
        ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{messages}"),
            ("human", user_prompt)])
        | llm
        | StrOutputParser()
    )
    
    # TODO: schema와 examples는 실제 값으로 대체해야 합니다.
    schema_placeholder = "column_name:type, column_name2:type"  # 임시 스키마
    examples_placeholder = "Question: 예시 질문\\nSQL: SELECT 예시_컬럼 FROM 예시_테이블" # 임시 예제

    sql_query_input = {
        "messages": state["messages"][:-1] if len(state["messages"]) > 1 else [],
        "input": state["messages"][-1].content if state["messages"][-1].type == "human" else "",
        "table_name": state["org_table_name"],
        "schema": schema_placeholder, # 임시 스키마 전달
        "examples": examples_placeholder # 임시 예제 전달
    }
    
    generated_sql = chain.invoke(sql_query_input).replace("medium_sample", state["org_table_name"])
    state["SQLquery"] = generated_sql # 생성된 SQL을 SQLquery 필드에 저장
    
    if state["org_table_name"] != "medium_sample":
        state["SQLquery"] = state["SQLquery"].replace("source_report", "SOURCE_REPORT").replace("page_report", "PAGE_REPORT").replace("event_report", "EVENT_REPORT")
    
    state["answer"] = state["SQLquery"] # 생성된 SQL 쿼리를 answer 필드에도 저장
    logger.info(f"transfer_TextToSQL: Generated SQL: {state['SQLquery']}") # 로그 추가

    return state

@lru_cache(maxsize=2)
def create_graph_chain():
    workflow = StateGraph(GraphState)
    workflow.add_node("categorized", categorized)
    workflow.add_node("judged_sql_query", judged_sql_query)
    workflow.add_node("roll_base_answer", roll_base_answer)
    workflow.add_node("transfer_date", transfer_date)
    workflow.add_node("transfer_TextToSQL", transfer_TextToSQL)
    workflow.add_node("missing_data_answer", missing_data_answer)

    workflow.add_conditional_edges(
        "categorized",
        lambda state: state["state"],
        {
            "SQLquery": "transfer_date",
            "block": "roll_base_answer",
            "out_of_scope": "roll_base_answer",
            "roll_base_answer": "roll_base_answer" # 알 수 없는 분류 결과 시
        }
    )
    workflow.add_conditional_edges(
        "transfer_date",
        lambda state: state["state"],
        {
            "out_of_date": "roll_base_answer", # 날짜가 유효하지 않으면 롤베이스 답변
            "transfer_date": "judged_sql_query" # 날짜 변환 성공 시 SQL 판단으로
        }
    )
    workflow.add_conditional_edges(
        "judged_sql_query",
        lambda state: state["answer"],
        {
            "True": "transfer_TextToSQL",
            "False": "missing_data_answer"
        }
    )
    workflow.set_entry_point("categorized")
    workflow.add_edge("transfer_TextToSQL", END)
    workflow.add_edge("missing_data_answer", END)
    workflow.add_edge("roll_base_answer", END)
    
    app = workflow.compile()
    return app

# 사용 예시 (테스트를 위해 추가, 실제 사용 시에는 제거)
if __name__ == '__main__':
    # 예시: 사용자가 "지난주 youtube 채널 방문자 수 알려줘" 라고 질문
    initial_state = GraphState(
        messages=[HumanMessage(content="지난주 youtube 채널 방문자 수 알려줘")],
        org_table_name="medium_sample", # 예시 테이블 이름
        state=None,
        SQLquery=None,
        chat_id="test_chat_id", # 예시 채팅 ID
        answer=None
    )

    # 그래프 체인 생성 (버전 명시 없이)
    graph_app = create_graph_chain()

    # 실행
    final_state = graph_app.invoke(initial_state)
    print(f"최종 상태: {final_state}")
    print(f"최종 답변: {final_state['answer']}")
    if final_state['SQLquery']:
        print(f"생성된 SQL 쿼리: {final_state['SQLquery']}") 