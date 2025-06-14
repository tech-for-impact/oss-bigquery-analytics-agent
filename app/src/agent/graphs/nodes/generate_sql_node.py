from src.core.state import TextToSQLState

# TODO: 간단한 SQL 생성 노드
def generate_simple_sql_node(state: TextToSQLState) -> dict:
	return {
		"sql_query": "SELECT * FROM events"
	}

# TODO: 집계 쿼리 생성 노드
def generate_aggregate_sql_node(state: TextToSQLState) -> dict:
	return {
		"sql_query": "SELECT COUNT(*) FROM events"
	}