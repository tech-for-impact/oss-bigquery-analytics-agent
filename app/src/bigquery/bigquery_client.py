from typing import Dict, Any
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

from app.src.core.settings import settings
from app.src.utils.logger import logger

class BigQueryClient:
    """Google BigQuery 클라이언트
    
    BigQuery API를 사용하여 쿼리를 실행하고 결과를 반환하는 클라이언트 클래스입니다.
    """
    
    def __init__(self):
        try:
            # 서비스 계정 키 파일 경로로부터 인증 정보 생성
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_APPLICATION_CREDENTIALS
            )

            # BigQuery 클라이언트 초기화
            self.client = bigquery.Client(
                credentials=credentials,
                project=settings.BIGQUERY_PROJECT_ID
            )
            logger.info("BigQuery 클라이언트 초기화 성공")
            
        except Exception as e:
            logger.error(f"BigQuery 클라이언트 초기화 실패: {str(e)}")
            raise

    async def execute_query(self, sql: str, chat_id: str) -> Dict[str, Any]:
        """SQL 쿼리를 실행하고 결과를 반환합니다.

        Args:
            sql (str): 실행할 SQL 쿼리문
            chat_id (str): 챗 ID.

        Returns:
            Dict[str, Any]: 쿼리 실행 결과를 포함하는 딕셔너리
            
        Raises:
            Exception: 쿼리 실행 중 오류 발생시
        """
        try:
            logger.info(f"Executing query for {chat_id}: {sql}")
            
            # 쿼리 작업 설정
            job_config = bigquery.QueryJobConfig()
            
            # 쿼리 작업 실행
            query_job = self.client.query(
                query=sql,
                job_config=job_config
            )
            
            # 결과 대기 및 가져오기
            results = query_job.result()
            
            # 결과를 딕셔너리 리스트로 변환
            rows = [dict(row.items()) for row in results]
            
            response = {
                "results": rows,
                "total_rows": results.total_rows,
                "job_id": query_job.job_id
            }
            
            logger.info(f"Query executed successfully. Total rows: {results.total_rows}")
            return response
            
        except Exception as e:
            error_msg = f"BigQuery 쿼리 실행 실패: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

# BigQuery 클라이언트 싱글톤 인스턴스
bigquery_client = BigQueryClient() 