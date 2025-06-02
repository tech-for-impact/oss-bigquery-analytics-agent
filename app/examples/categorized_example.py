"""
CategorizedPrompt 및 CategorizedFewShotPrompt 테스트

categorized.yml과 categorized_few_shot.yml 파일이 정상적으로 로드되고 작동하는지 확인합니다.
두 가지 방식의 차이점을 비교할 수 있습니다.
"""

import sys
import os
from pathlib import Path

# 상위 디렉토리의 src 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 작업 디렉토리를 app 디렉토리로 변경 (상대 경로 문제 해결)
app_dir = os.path.join(os.path.dirname(__file__), '..')
os.chdir(app_dir)

# prompt_loader의 PROMPT_DIR을 올바른 경로로 수정
from src.core import prompt_loader
prompt_loader.PROMPT_DIR = Path('prompts')  # 'app/prompts' 대신 'prompts' 사용

from src.prompt_templates.categorized import CategorizedPrompt
from src.prompt_templates.categorized_few_shot import CategorizedFewShotPrompt


def run_comparison_test():
    """
    두 방식의 차이점을 비교하는 테스트
    """
    test_input = "마케팅 채널별 성과 비교 분석"
    
    try:
        # 일반 프롬프트
        categorized_prompt = CategorizedPrompt()
        normal_result = categorized_prompt.get_prompt(user_input=test_input)
        
        # Few-shot 프롬프트  
        few_shot_prompt = CategorizedFewShotPrompt()
        few_shot_result = few_shot_prompt.get_prompt(user_input=test_input)
        
        print("--- categorized 프롬프트 ---")
        print(normal_result)
        print()
        print("--- categorized-few-shot 프롬프트 ---")
        print(few_shot_result)
        
    except Exception as e:
        print(f"❌ 비교 테스트 실패: {e}")


if __name__ == "__main__":
    run_comparison_test() 