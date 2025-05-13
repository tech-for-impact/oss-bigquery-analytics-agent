#!/usr/bin/env python3

import os
import sys
from datetime import datetime
import yaml

def create_prompt_file(prompt_type: str, filename: str) -> None:
    """
    프롬프트 파일을 생성합니다.
    
    Args:
        prompt_type (str): 프롬프트의 종류
        filename (str): 파일 이름
    """
    # 현재 시간을 yyyyMMddHHmmss 형식으로 가져옴
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 프롬프트 파일이 저장될 디렉토리 경로
    base_dir = os.path.join("prompts")
    prompt_dir = os.path.join(base_dir, prompt_type)
    
    # 디렉토리가 없으면 생성
    os.makedirs(prompt_dir, exist_ok=True)
    
    # 파일 경로 생성
    file_path = os.path.join(prompt_dir, f"{timestamp}_{filename}.yml")
    
    # 기본 프롬프트 템플릿
    prompt_template = {
        "name": filename,
        "type": prompt_type,
        "created_at": timestamp,
        "content": {
            "system": "",
            "user": "",
            "assistant": ""
        }
    }
    
    # YAML 파일로 저장
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(prompt_template, f, allow_unicode=True, sort_keys=False)
    
    print(f"프롬프트 파일이 생성되었습니다: {file_path}")

def main():
    # 프롬프트 종류 입력 받기
    prompt_type = input("프롬프트 종류를 입력하세요: ").strip()
    if not prompt_type:
        print("프롬프트 종류는 필수입니다.")
        sys.exit(1)
    
    # 파일 이름 입력 받기
    filename = input("파일 이름을 입력하세요: ").strip()
    if not filename:
        print("파일 이름은 필수입니다.")
        sys.exit(1)
    
    # 프롬프트 파일 생성
    create_prompt_file(prompt_type, filename)

if __name__ == "__main__":
    main()