# app/src/core/prompt_template_registry.py

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, Optional

from src.core.custom_base_template import CustomBaseTemplate

class PromptTemplateRegistry:
    """
    app/src/prompt_templates 디렉터리 내부에서 CustomBaseTemplate을 상속받은 모든 클래스들을 찾아
    인스턴스를 생성하여 {prompt_name: instance} 형태의 딕셔너리로 보관합니다.
    """

    def __init__(self):
        # 실제 템플릿 객체를 담을 딕셔너리: { prompt_name (str) : CustomBaseTemplate 인스턴스 }
        self.templates: Dict[str, 'CustomBaseTemplate'] = {}

    @classmethod
    async def create(cls):
        """비동기 팩토리 메서드 - PromptTemplateRegistry 인스턴스를 생성하고 초기화합니다."""
        instance = cls()
        await instance._discover_and_load()
        return instance

    async def _discover_and_load(self):
        """
        app/src/prompt_templates 디렉터리를 스캔하여, 사용자가 정의한 모든 모듈을 import하고,
        그 안에서 CustomBaseTemplate을 상속받은 클래스를 찾아 인스턴스를 생성해 self.templates에 저장한다.
        """
        # Import CustomBaseTemplate locally to avoid circular import
        from src.core.custom_base_template import CustomBaseTemplate

        # 현재 파일(__file__) 위치: app/src/core/prompt_template_registry.py
        # prompt_templates 폴더 경로: app/src/prompt_templates
        base_dir = Path(__file__).parent.parent / "prompt_templates"
        if not base_dir.is_dir():
            raise RuntimeError(f"prompt_templates 디렉터리가 존재하지 않습니다: {base_dir}")

        # Python 패키지 경로로 변환: 예) app.src.prompt_templates
        # (만약 src가 PYTHONPATH에 포함되어 있다면, 패키지명은 prompt_templates만 되어야 할 수도 있음)
        # 여기에선 프로젝트 최상위 디렉터리가 PYTHONPATH에 포함되어 있다고 가정하고 "app.src.prompt_templates"를 사용
        package_root = "src.prompt_templates"

        # prompt_templates 디렉터리 내의 모든 .py 모듈을 반복
        for finder, module_name, ispkg in pkgutil.iter_modules([str(base_dir)]):
            if module_name.startswith("_"):
                # __init__.py나 private 모듈은 건너뜀
                continue

            full_module_name = f"{package_root}.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
            except ImportError as e:
                # import 에 실패하면 로그를 남기거나 무시할 수 있음
                print(f"ImportError: {e}")
                continue

            # 모듈 내부에 정의된 클래스들 중 CustomBaseTemplate을 상속받은 것만 골라낸다
            for obj_name, obj in inspect.getmembers(module, inspect.isclass):
                # obj.__module__을 확인하여, 순수하게 이 모듈에서 정의된 클래스인지 확인
                if obj.__module__ != full_module_name:
                    continue

                # CustomBaseTemplate을 상속받았는지 검사 (단, CustomBaseTemplate 자신은 제외)
                if issubclass(obj, CustomBaseTemplate) and obj is not CustomBaseTemplate:
                    instance: CustomBaseTemplate = await obj.create()  # 비동기 팩토리 메서드 사용
                    prompt_name = getattr(instance, "prompt_name", None)
                    if not prompt_name:
                        # prompt_name 속성이 누락되었다면 건너뜀
                        continue

                    # 중복 키가 있는지 확인
                    if prompt_name in self.templates:
                        raise RuntimeError(f"중복된 prompt_name이 발견되었습니다: {prompt_name}")

                    self.templates[prompt_name] = instance

    def get_all_prompt_names(self) -> list[str]:
        """현재 로드된 모든 템플릿의 prompt_name 리스트를 반환"""
        return list(self.templates.keys())

    def get_template_by_name(self, name: str) -> Optional['CustomBaseTemplate']:
        """
        prompt_name으로 템플릿 객체를 조회하여 반환.
        없으면 None을 반환.
        """
        return self.templates.get(name)
