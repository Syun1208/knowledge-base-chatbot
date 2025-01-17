from abc import ABC, abstractmethod
from typing import List

class LLM(ABC):
    
    @abstractmethod 
    def generate(self, prompt: str, conversation: List[str]) -> str:
        pass
