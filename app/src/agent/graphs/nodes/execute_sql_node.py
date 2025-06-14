from src.core.state import TextToSQLState


def execute_sql_node(state: TextToSQLState):
    """생성된 SQL 실행"""
    # 실제 구현시 데이터베이스 연결 로직 추가[2]
    sample_data = [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"}
    ]
    return {"query_result": sample_data}
