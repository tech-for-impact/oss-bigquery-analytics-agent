"""
프롬프트 템플릿 모듈

이 모듈은 다양한 프롬프트 템플릿 클래스들을 제공합니다.
모든 템플릿은 CustomBaseTemplate을 상속받아 구현됩니다.
"""

from .categorized import CategorizedPrompt

__all__ = [
    "CategorizedPrompt"
]
