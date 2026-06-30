from .base import BaseLLM


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
        prompt: str
    ):

        return self.client.invoke(
            prompt
        )