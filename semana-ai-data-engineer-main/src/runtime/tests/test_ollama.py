from ..llm.ollama import OllamaLLM
from src.runtime.prompt.prompt import Prompt

llm = OllamaLLM()

response = llm.invoke(
    Prompt("Say hello in one sentence.")
)

print()

print("=" * 80)
print("OLLAMA RESPONSE")
print("=" * 80)

print(response)