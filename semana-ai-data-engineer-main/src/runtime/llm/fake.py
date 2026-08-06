from .base import BaseLLM
from src.runtime.prompt.prompt import Prompt

class FakeLLM(BaseLLM):

    def invoke(
        self,
        prompt: Prompt
    ):
        print(">>> USING FAKE LLM <<<")
        return f"""
PROMPT RECEIVED

-------------------------

{prompt.text[:1000]}

-------------------------

END
"""