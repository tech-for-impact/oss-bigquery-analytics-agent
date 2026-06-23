import pytest 

from src.agent.bigquery.client import BigQueryClient

@pytest.fixture
def bigquery_client():
    bq_client = BigQueryClient()
    client = bq_client.client
    yield bq_client, client

def mock_run_query(bigquery_client):
    bq_client, client = bigquery_client
    result = bq_client.run_query("SELECT 1 as test_column")

    assert result.success is True
    assert len(result.data) == 1


