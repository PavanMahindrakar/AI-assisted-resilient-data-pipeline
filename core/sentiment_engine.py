# core/sentiment_engine.py

# 🔹NEW FEATURE 4: LLM Abstraction Layer
# The DAG interacts with an abstract sentiment engine interface
# instead of calling the Ollama client directly, allowing the LLM
# backend to be swapped without changing DAG logic.

from abc import ABC, abstractmethod
from core.response_parser import parse_ollama_response  # if you split this

class SentimentEngine(ABC):
    @abstractmethod
    def analyze(self, text: str) -> dict:
        pass


class OllamaSentimentEngine(SentimentEngine):
    def __init__(self, model_name: str, host: str):
        import ollama
        self.client = ollama.Client(host=host)
        self.model = model_name

    def analyze(self, text: str) -> dict:
        response = self.client.chat(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"""
                Analyze sentiment as POSITIVE, NEGATIVE, or NEUTRAL.
                Review: "{text}"
                Reply ONLY as JSON:
                {{"sentiment":"POSITIVE","confidence":0.95}}
                """
            }],
            options={"temperature": 0.1}
        )
        return parse_ollama_response(response["message"]["content"])
