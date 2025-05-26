import os
import yaml

PROMPT_DIR = os.path.join(os.path.dirname(__file__), '../../prompts')

class PromptRegistry:
    def __init__(self, prompt_dir: str = PROMPT_DIR):
        self.prompt_dir = os.path.abspath(prompt_dir)
        self.prompts = self._load_all_prompts()

    def _load_all_prompts(self):
        prompts = {}
        for fname in os.listdir(self.prompt_dir):
            if fname.endswith('.yaml'):
                with open(os.path.join(self.prompt_dir, fname), encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    # 파일명에서 확장자를 제거하여 키로 사용
                    prompt_name = os.path.splitext(fname)[0]  # 확장자 제거
                    prompts[prompt_name] = data
        return prompts

    def get_prompt(self, name: str, **kwargs) -> str:
        prompt = self.prompts.get(name)
        if not prompt:
            raise ValueError(f"Prompt '{name}' not found.")
        template = prompt['template']
        # 템플릿 간단 치환 (고도화 시 Jinja2 추천)
        for k, v in kwargs.items():
            template = template.replace(f"{{{k}}}", str(v))
        return template

    def list_prompts(self):
        """사용 가능한 프롬프트 목록 반환"""
        return list(self.prompts.keys())

    def reload(self):
        self.prompts = self._load_all_prompts()

# 싱글톤 인스턴스 (사용 권장)
prompt_registry = PromptRegistry()

if __name__ == "__main__":
    prompt_registry = PromptRegistry()
    print(prompt_registry.get_prompt("categorized", input="테스트입니다."))