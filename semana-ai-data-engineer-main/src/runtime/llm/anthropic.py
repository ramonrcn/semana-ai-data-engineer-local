from .base import BaseLLM
from src.runtime.prompt.prompt import Prompt

class AnthropicLLM(
    BaseLLM
):

    def __init__(
        self,
        client
    ):
        self.client = client

    def invoke(
        self,
        prompt: Prompt
    ):

        return self.client.invoke(
            prompt.text
        )