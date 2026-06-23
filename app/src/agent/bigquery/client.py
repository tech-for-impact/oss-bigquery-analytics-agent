from google.cloud import bigquery
from .configuration import settings

class BigQueryResult:
    def __init__(self, success: bool, data=None, error:str=None):
        self.success = success
        self.data = data
        self.error = error

class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client(
            project=settings.project_id,
        )
    
    def run_query(self, sql:str) -> BigQueryResult:
        try:
            query_job = self.client.query(sql)
            results = query_job.result()
            rows = [dict(row.items()) for row in results]
            return BigQueryResult(success=True, data=rows)
        except Exception as e:
            return BigQueryResult(success=False, error=str(e))

