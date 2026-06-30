from .base import BaseLLM


class FakeLLM(BaseLLM):

    def invoke(
        self,
        prompt: str
    ):
        print(">>> USING FAKE LLM <<<")
        return f"""
PROMPT RECEIVED

-------------------------

{prompt[:1000]}

-------------------------

END
"""