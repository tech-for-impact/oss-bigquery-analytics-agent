from datetime import datetime
import re
import calendar

from .logger import logger # 수정된 임포트 경로

def format_date(date: datetime) -> str:
    """주어진 날짜를 문자열 형식으로 변환합니다.

    Args:
        date (datetime): 변환할 날짜 객체.

    Returns:
        str: 변환된 날짜 문자열 (형식: "Month Day, Year").
    """
    months = {
        1: "January",   2: "February", 3: "March",     4: "April",
        5: "May",       6: "June",     7: "July",      8: "August",
        9: "September", 10: "October", 11: "November", 12: "December",
    }
    return f"{months[date.month]} {date.day}, {date.year}"

def check_query_date(query: str) -> bool:
    """
    정규식을 사용하여 사용자 쿼리에서 날짜 패턴을 추출하고 2024년 1월 1일 이전인지 확인합니다.
    
    Args:
        query: 사용자 쿼리 문자열
    
    Returns:
        bool: 유효한 날짜인지 여부 (2024년 1월 1일 이전이면 False)
    """
    min_date = datetime(2024, 1, 1)
    
    # 단순 연도 검사 - 제일 먼저 확인 (2023, 2023년)
    year_only_patterns = [
        r'\b(19\d{2}|20[0-2]\d)\b',  # 2023과 같은 숫자만 있는 연도
        r'\b(19\d{2}|20[0-2]\d)[-./년]',  # 2023년과 같은 형식
        r'\b(\d{2})[-./년]',  # 23년과 같은 약식 표현
    ]
    
    # 연도만 확인
    for pattern in year_only_patterns:
        matches = re.findall(pattern, query)
        for match in matches:
            try:
                # 숫자 부분만 추출
                year_str = re.sub(r'[-./년]', '', match)
                year = int(year_str)
                
                # 두 자리 연도 처리
                if len(year_str) == 2:
                    year += 2000 if year < 50 else 1900
                
                if year < 2024:
                    return False
            except Exception as e:
                logger.error(f"Error processing year only: {e}")
    
    # 연도를 포함한 날짜 패턴 (2023년 12월 31일, 2023-12-31, 2023/12/31 등)
    year_patterns = [
        r'(\d{4})[-./년]\s*(\d{1,2})[-./월]\s*(\d{1,2})[일]?',  # 2023-12-31, 2023년 12월 31일
        r'(\d{2})[-./년]\s*(\d{1,2})[-./월]\s*(\d{1,2})[일]?',  # 23-12-31, 23년 12월 31일
    ]
    
    # 연도-월 패턴 (2023년 8월, 23년 8월 등)
    year_month_patterns = [
        r'(\d{4})[-./년]\s*(\d{1,2})[-./월]',  # 2023년 8월, 2023-8
        r'(\d{2})[-./년]\s*(\d{1,2})[-./월]',  # 23년 8월, 23-8
    ]
    
    # 상대적 날짜 표현 (작년, 올해, 저번 달, 지난해 등)
    relative_patterns = {
        r'작년|지난[\s]*해|전[\s]*해|저번[\s]*해': -1,  # 작년은 현재 연도에서 -1
        r'올해|금년|이번[\s]*해': 0,              # 올해는 현재 연도 그대로
        r'내년|다음[\s]*해|다가올[\s]*해': 1      # 내년은 현재 연도에서 +1
    }
    
    # 쿼리에서 모든 연도 포함 날짜 패턴 검색
    for pattern in year_patterns:
        matches = re.findall(pattern, query)
        for match in matches:
            try:
                year = int(match[0])
                if len(match[0]) == 2:  # 두 자리 연도인 경우 (23년)
                    year += 2000 if year < 50 else 1900
                
                month = int(match[1])
                day = int(match[2])
                
                # 유효한 날짜인지 확인
                if month > 0 and month <= 12 and day > 0 and day <= calendar.monthrange(year, month)[1]:
                    date = datetime(year, month, day)
                    if date < min_date:
                        return False
            except Exception as e:
                logger.error(f"Error processing date: {e}")
                continue
    
    # 연도-월 패턴 검색 (일 정보 없는 경우)
    for pattern in year_month_patterns:
        matches = re.findall(pattern, query)
        for match in matches:
            try:
                year = int(match[0])
                if len(match[0]) == 2:  # 두 자리 연도인 경우 (23년)
                    year += 2000 if year < 50 else 1900
                
                month = int(match[1])
                
                # 유효한 월인지 확인
                if month > 0 and month <= 12:
                    # 해당 월의 1일로 날짜 설정
                    date = datetime(year, month, 1)
                    if date < min_date:
                        return False
            except Exception as e:
                logger.error(f"Error processing year-month: {e}")
                continue
    
    # 현재 날짜 기준
    now = datetime.now()
    current_year = now.year
    
    # 상대적 날짜 표현 처리
    for pattern, year_offset in relative_patterns.items():
        if re.search(pattern, query):
            ref_year = current_year + year_offset
            if ref_year < 2024:  # 2024년 이전 연도 참조
                return False
    
    # 모든 검사를 통과했으면 유효한 날짜로 간주
    return True 