from src.core.state import TextToSQLState
from langgraph.graph import StateGraph, END
from src.agent.graphs.nodes.execute_sql_node import execute_sql_node
from src.agent.graphs.nodes.general_response_node import general_response_node
from src.agent.graphs.nodes.intent_classification_node import intent_classification_node
from src.agent.graphs.nodes.generate_sql_node import generate_simple_sql_node, generate_aggregate_sql_node

def text_to_sql_graph(input_text: str) -> dict:
	builder = StateGraph(TextToSQLState)
	# 노드 추가
	builder.add_node("intent_classification", intent_classification_node)
	builder.add_node("general_response", general_response_node)
	builder.add_node("generate_simple_sql", generate_simple_sql_node)
	builder.add_node("generate_aggregate_sql", generate_aggregate_sql_node)
	builder.add_node("execute_sql", execute_sql_node)

	# 시작 노드 설정
	builder.set_entry_point("intent_classification")

	# 조건부 엣지 추가
	builder.add_conditional_edges(
		"intent_classification",
		lambda state: state["intent"],
		{
			"SIMPLE_QUERY": "generate_simple_sql",
			"AGGREGATE_QUERY": "generate_aggregate_sql",
			"GENERAL": "general_response",
		}
	)

	# 엣지 추가
	builder.add_edge("generate_simple_sql", "execute_sql")
	builder.add_edge("generate_aggregate_sql", "execute_sql")

	# 종료 노드 설정
	builder.add_edge("general_response", END)
	builder.add_edge("execute_sql", END)
	
	# 그래프 컴파일
	graph = builder.compile()
	
	# 그래프 실행
	return graph.invoke({"messages": [{"role": "user", "content": input_text}]})
	