from src.core.custom_base_template import CustomBaseTemplate

class PromptTemplateRegistry(type):
    _registry: dict[str, object] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # BaseTemplate 자체는 등록하지 않음
        if bases and bases != (object,):
            prompt_name = getattr(cls, "prompt_name", None) or name
            PromptTemplateRegistry._registry[prompt_name] = cls()
        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, CustomBaseTemplate]:
        """현재 등록된 모든 프롬프트 템플릿 반환"""
        return dict(mcs._registry)

    @classmethod
    def register(mcs, name: str, template: CustomBaseTemplate):
        """
        수동으로 프롬프트 템플릿을 레지스트리에 추가
        name: 레지스트리 키
        template: CustomBaseTemplate 인스턴스
        """
        mcs._registry[name] = template
