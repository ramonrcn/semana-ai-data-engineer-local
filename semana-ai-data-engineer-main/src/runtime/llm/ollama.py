from openai import OpenAI
from .base import BaseLLM
from src.runtime.prompt.prompt import Prompt


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model= "qwen2.5-coder:7b",
        base_url="http://localhost:11435/v1"
    ):

        self.model = model

        self.client = OpenAI(

            base_url=base_url,

            api_key="ollama"

        )

    def invoke(
        self,
        prompt: Prompt
    ):
        print(f">>> USING OLLAMA: {self.model} <<<")
        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt.text
                }
            ]

        )

        return response.choices[0].message.content