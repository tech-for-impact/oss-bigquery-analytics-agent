# app/src/core/prompt_template_manager.py

from typing import Optional

from src.core.prompt_template_registry import PromptTemplateRegistry
from src.core.custom_base_template import CustomBaseTemplate  # Corrected import path


class PromptTemplateManager:
    """
    PromptTemplateRegistry의 라이프사이클을 관리하고, FastAPI 실행 시
    템플릿을 메모리에 로드하거나 조회하는 기능을 제공한다.
    """

    _registry: Optional[PromptTemplateRegistry] = None

    @classmethod
    async def init_prompt_registry(cls) -> None:
        """
        앱 시작 시 한 번 호출되어야 하며, PromptTemplateRegistry를 초기화하여
        모든 CustomBaseTemplate 기반 템플릿을 메모리에 로드한다.
        """
        if cls._registry is None:
            cls._registry = await PromptTemplateRegistry.create()

    @classmethod
    def find_prompt_template(cls, prompt_name: str) -> CustomBaseTemplate:
        """
        prompt_name으로 템플릿을 조회하여 반환.
        registry가 초기화되지 않았거나, 해당 이름의 템플릿이 없으면 KeyError를 발생시킨다.
        """
        if cls._registry is None:
            raise RuntimeError("PromptTemplateRegistry가 초기화되지 않았습니다. init_prompt_registry()를 먼저 호출하세요.")

        template = cls._registry.get_template_by_name(prompt_name)
        if template is None:
            raise KeyError(f"'{prompt_name}'에 해당하는 PromptTemplate을 찾을 수 없습니다.")
        return template

    @classmethod
    def list_all_templates(cls) -> list[str]:
        """
        현재 로드된 모든 prompt_name 리스트를 반환.
        """
        if cls._registry is None:
            return []
        return cls._registry.get_all_prompt_names()
