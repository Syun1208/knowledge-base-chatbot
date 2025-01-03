from abc import ABC, abstractmethod


class RAG(ABC):
    
    @abstractmethod
    def invoke(self, query: str) -> None:
        pass