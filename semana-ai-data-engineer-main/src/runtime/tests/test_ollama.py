from ..llm.ollama import OllamaLLM


llm = OllamaLLM()

response = llm.invoke(
    "Say hello in one sentence."
)

print()

print("=" * 80)
print("OLLAMA RESPONSE")
print("=" * 80)

print(response)