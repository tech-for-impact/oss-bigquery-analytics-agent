#!/usr/bin/env python3

import os
import sys
import shutil
from datetime import datetime
import yaml

# 스크립트 파일 위치를 기준으로 prompts 폴더 경로 계산
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(SCRIPT_DIR, "..", "prompts")
PROMPTS_DIR = os.path.abspath(PROMPTS_DIR)

def ensure_directories():
    """필요한 디렉토리들을 생성합니다."""
    os.makedirs(PROMPTS_DIR, exist_ok=True)

def copy_existing_prompts():
    """기존 prompts 폴더의 yaml 파일들을 현재 시간 기준 폴더로 복사합니다."""
    ensure_directories()
    
    # 현재 시간을 기준으로 폴더명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_dir = os.path.join(PROMPTS_DIR, f"generated_{timestamp}")
    
    # 타임스탬프 폴더 생성
    os.makedirs(timestamped_dir, exist_ok=True)
    
    # 기존 yaml 파일들 복사
    yaml_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.yaml')]
    
    if not yaml_files:
        print("복사할 yaml 파일이 없습니다.")
        return None
    
    for yaml_file in yaml_files:
        src_path = os.path.join(PROMPTS_DIR, yaml_file)
        dst_path = os.path.join(timestamped_dir, yaml_file)
        
        # 파일 복사
        shutil.copy2(src_path, dst_path)
        print(f"파일 복사됨: {dst_path}")
    
    print(f"모든 프롬프트 파일이 생성됨: {timestamped_dir}")
    return timestamped_dir

def main():
    copy_existing_prompts()

if __name__ == "__main__":
    main()