import requests
from typing import List
from src.service.interface.kcb_supporter.llm import LLM


class Ollama(LLM):
    def __init__(self) -> None:
        super(Ollama, self).__init__()
        self.url = 'http://localhost:5000/api/generate'

    def generate(self, prompt: str, conversation: List[str]) -> str:
        response = requests.post(
            self.url,
            json={
                'prompt': prompt,
                'context': conversation,
            },
            stream=True
        )
        response.raise_for_status()

        return response
