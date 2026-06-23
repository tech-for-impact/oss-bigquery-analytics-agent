import os
from google.cloud import bigquery
from typing import Optional, List
from dotenv import load_dotenv

# Set credentials for BigQuery
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

class QueryResult:
    def __init__(self, is_success:bool, data: Optional[List[dict]] = None, error: Optional[str] = None):
        """
        Represents the result of a BigQuery query.
        
        Args:
            is_success (bool): Whether the query was successful.
            data (Optional[List[dict]]): Resulting data rows (if successful).
            error (Optional[str]): Error message (if failed).
        """
        self.is_success = is_success
        self.data = data
        self.error = error
    
    def __repr__(self):
        return f"<QueryResult success={self.is_success} rows={len(self.data) if self.data else 0} error={self.error}>"

class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client()
        
    def run_query(self, sql:str):
        """
        Executes a SQL query on BigQuery.

        Args:
            sql (str): The SQL query string.

        Returns:
            QueryResult: Object containing query success status, data, or error message.
        """
        
        try:
            query_job = self.client.query(sql)
            results = query_job.result()
            rows = [dict(row.items()) for row in results]
            return QueryResult(is_success=True, data=rows)

        except Exception as e:
            return QueryResult(is_success=False, error=str(e))

if __name__ == "__main__":
    client = BigQueryClient()
    
    project_id = 'ai-agent-461500'
    dataset_id = 'ga_sample'
    table_id = 'events_20250530'
    sql = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}` LIMIT 5"
    
    result = client.run_query(sql)
    if result.is_success:
        for row in result.data:
            print(row)
    else:
        print("Query failed:", result.error)