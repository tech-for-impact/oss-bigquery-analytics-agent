# prompt_manager.py

import pkgutil
import importlib
from src.core.prompt_template_registry import PromptTemplateRegistry
from src.core.custom_base_template import CustomBaseTemplate

class PromptTemplateManager:
    @staticmethod
    def load_all_templates(package: str):
        """
        주어진 패키지 내 모든 모듈을 임포트하여
        CustomBaseTemplate 서브클래스들의 자동 등록을 트리거합니다.
        """
        pkg = importlib.import_module(package)
        for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
            importlib.import_module(f"{package}.{modname}")

    @staticmethod
    def get_template(name: str) -> CustomBaseTemplate | None:
        """
        등록된 프롬프트 템플릿 인스턴스를 반환
        name: prompt_name 키
        """
        return PromptTemplateRegistry.get_registry().get(name)
